import os
import pyinotify
import subprocess
from shutil import copyfile
import GPUtil
import glob
import os
from utils import prepare_result_dir
import configs
from time import sleep, ctime
import sys
import run_ZSSR_single_input
SOURCE = 'police_video_frames'
TEST_DATA = 'test_data'


class EventHandler(pyinotify.ProcessEvent):

    BATCH_SIZE = 5

    def __init__(self, results_dir, all_frames_to_create, conf, local_dir, cur_gpu, conf_name):
        super(EventHandler, self).__init__()
        self.results_dir = results_dir
        self.all_frames = all_frames_to_create
        self.running_frames = []
        self.finished_frames = []
        self.counter = 0
        # run configurations
        self.conf = conf
        self.local_dir = local_dir
        self.cur_gpu = cur_gpu
        self.conf_name = conf_name

    def process_IN_CREATE(self, event):
        print("Created:", event.pathname)
        if event.pathname in self.all_frames:
            self.all_frames.remove(event.pathname)
            print(f"Removing {event.pathname} from all frames list.")
            self.finished_frames.append(event.pathname)
            self.counter -= 1
            while self.counter < self.BATCH_SIZE:
                self.counter += 1
                self.all_frames.sort(key=lambda x: int(x.split("frame")[-1].split("_zssr_X2.00X2.00.png")[0]))
                print(f"{len(self.all_frames)} frames remaining to process")
                for frame in self.all_frames[:self.BATCH_SIZE]:
                    if frame not in self.running_frames:
                        input_file = "test_data/" + frame.split("_zssr_X2.00X2.00.png")[0].split(self.results_dir + "/")[-1] + ".png"
                        os.system("xterm -e " + self.conf.python_path +
                                  f" {self.local_dir}/run_ZSSR_single_input.py '{input_file}' '{0}' '{0}' '{self.cur_gpu}' '{self.conf_name}' '{self.results_dir}' alias python &")
                        print(ctime())
                        self.running_frames.append(frame)
                        print(f"Running frame which will result in : {frame}")
                if not self.all_frames:
                    print("Done creating frames")


def main_watcher():
    # The watch manager stores the watches and provides operations on watches
    watch_manager = pyinotify.WatchManager()

    mask = pyinotify.IN_CREATE  # watched events

    all_frames = [f"/tmp/frame{i}.png" for i in range(10)]
    handler = EventHandler(all_frames)
    notifier = pyinotify.Notifier(watch_manager, handler)
    wdd = watch_manager.add_watch('/tmp', mask, rec=True)

    notifier.loop()


def main(conf_name, gpu):
    # Initialize configs and prepare result dir with date
    if conf_name is None:
        conf = configs.Config()
    else:
        conf = None
        conf_string_to_conf = {'X2_REAL_CONF': configs.X2_REAL_CONF,
                               'X2_GIVEN_KERNEL_CONF': configs.X2_GIVEN_KERNEL_CONF,
                               'X2_GRADUAL_IDEAL_CONF': configs.X2_GRADUAL_IDEAL_CONF,
                               'X2_IDEAL_WITH_PLOT_CONF': configs.X2_IDEAL_WITH_PLOT_CONF,
                               'X2_ONE_JUMP_IDEAL_CONF': configs.X2_ONE_JUMP_IDEAL_CONF}
        conf = conf_string_to_conf[conf_name]
    res_dir = prepare_result_dir(conf)
    local_dir = os.path.dirname(__file__)

    # We take all png files that are not ground truth
    files = [file_path for file_path in glob.glob('%s/*.png' % conf.input_path)
             if not file_path[-7:-4] == '_gt']

    # Loop over all the files
    for file_ind, input_file in enumerate([files[0]]):

        # Ground-truth file needs to be like the input file with _gt (if exists)
        ground_truth_file = input_file[:-4] + '_gt.png'
        if not os.path.isfile(ground_truth_file):
            ground_truth_file = '0'

        # Numeric kernel files need to be like the input file with serial number
        kernel_files = ['%s_%d.mat;' % (input_file[:-4], ind) for ind in range(len(conf.scale_factors))]
        kernel_files_str = ''.join(kernel_files)
        for kernel_file in kernel_files:
            if not os.path.isfile(kernel_file[:-1]):
                kernel_files_str = '0'
                print('no kernel loaded')
                break

        print(kernel_files)

        # This option uses all the gpu resources efficiently
        if gpu == 'all':
            # Stay stuck in this loop until there is some gpu available with at least half capacity
            gpus = []
            while not gpus:
                gpus = GPUtil.getAvailable(order='memory')

            # Take the gpu with the most free memory
            cur_gpu = gpus[-1]
            print(f"local_dir = {local_dir}")
            if local_dir == "" or local_dir is None:
                local_dir = "."

            # # Run ZSSR from command line, open xterm for each run
            # os.system("xterm -hold -e " + conf.python_path +
            #           f" {local_dir}/run_ZSSR_single_input.py '{input_file}' '{ground_truth_file}' '{kernel_files_str}' '{cur_gpu}' '{conf_name}' '{res_dir}' alias python &")
            #           # % (local_dir, input_file, ground_truth_file, kernel_files_str, cur_gpu, conf_name, res_dir))
            os.system("xterm -e " + conf.python_path +
                       f" {local_dir}/create_dummy.py '{res_dir}' alias python &")
            # Verbose
            print('Ran file #%d: %s on GPU %d\n' % (file_ind, input_file, cur_gpu))

            # Wait 5 seconds for the previous process to start using GPU. if we wouldn't wait then GPU memory will not
            # yet be taken and all process will start on the same GPU at once and later collapse.
            sleep(5)

        # The other option is just to run sequentially on a chosen GPU.
        else:
            run_ZSSR_single_input.main(input_file, ground_truth_file, kernel_files_str, gpu, conf_name, res_dir)

        # The watch manager stores the watches and provides operations on watches
        watch_manager = pyinotify.WatchManager()

        mask = pyinotify.IN_CREATE  # watched events
        all_result_files = ['%s/%s_zssr_X2.00X2.00.png' %
                           (res_dir, os.path.basename(file)[:-4]) for file in files]
        all_result_files.append(os.path.abspath('%s/DUMMY.txt' % res_dir))
        handler = EventHandler(res_dir, all_result_files, conf, local_dir, cur_gpu, conf_name)
        notifier = pyinotify.Notifier(watch_manager, handler)
        wdd = watch_manager.add_watch(res_dir, mask, rec=True)

        notifier.loop()


if __name__ == '__main__':
    conf_str = sys.argv[1] if len(sys.argv) > 1 else None
    gpu_str = sys.argv[2] if len(sys.argv) > 2 else None
    main(conf_str, gpu_str)
