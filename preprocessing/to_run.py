self.input = img.imread("police_video_frames/cropped/frame1000.png")
post_processed_output = self.final_test()
self.hr_fathers_sources.append(post_processed_output)
self.base_change()
# Save the final output if indicated
sf_str = ''.join('X%.2f' % s for s in self.conf.scale_factors[self.sf_ind])
plt.imsave('%s/%s_zssr_%s.png' % (self.conf.result_path, os.path.basename(self.file_name)[:-4], sf_str),post_processed_output, vmin=0, vmax=1)

################################
### FRAME 1001 ###
################################
self.input = img.imread("police_video_frames/cropped/frame1001.png")
post_processed_output = self.final_test()
self.hr_fathers_sources.append(post_processed_output)
self.base_change()
# Save the final output if indicated
sf_str = ''.join('X%.2f' % s for s in self.conf.scale_factors[self.sf_ind])
plt.imsave('%s/%s_zssr_%s.png' % (self.conf.result_path, "frame1001", sf_str), post_processed_output, vmin=0, vmax=1)

for i in range(990, 1100):
    self.input = img.imread(f"police_video_frames/cropped/frame{i}.png")
    post_processed_output = self.final_test()
    self.hr_fathers_sources.append(post_processed_output)
    self.base_change()
    # Save the final output if indicated
    sf_str = ''.join('X%.2f' % s for s in self.conf.scale_factors[self.sf_ind])
    plt.imsave('%s/%s_zssr_%s.png' % (self.conf.result_path, f"frame{i}", sf_str), post_processed_output, vmin=0, vmax=1)


for i in range(830, 990):
    self.input = img.imread(f"police_video_frames/cropped/frame{i}.png")
    post_processed_output = self.final_test()
    self.hr_fathers_sources.append(post_processed_output)
    self.base_change()
    # Save the final output if indicated
    sf_str = ''.join('X%.2f' % s for s in self.conf.scale_factors[self.sf_ind])
    plt.imsave('%s/%s_zssr_%s.png' % (self.conf.result_path, f"frame{i}", sf_str), post_processed_output, vmin=0, vmax=1)




# An example for a typical setup for real images. (Kernel needed + mild unknown noise)
# back-projection is not recommended because of the noise.
class X2_REAL_CONF(Config):
    def __init__(self):
        super().__init__()
        self.output_flip = False
        self.back_projection_iters = [0]
        self.input_path = os.path.dirname(__file__) + '/real_example'
        self.noise_std = 0.0125
        self.augment_allow_rotation = False
        self.augment_scale_diff_sigma = 0
        self.augment_shear_sigma = 0
        self.augment_min_scale = 0.75


################################
######## BASH TO RUN ###########
################################
mv /tmp/frame953.png test_data/
mv /tmp/frame954.png test_data/
date; python run_ZSSR.py X2_REAL_CONF

