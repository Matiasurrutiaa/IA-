from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
import torch
import warnings
import matplotlib.pyplot as plt

# Set device
device.set(device=DeviceId.GPU0)

# Setup
plt.style.use('dark_background')
torch.backends.cudnn.benchmark = True
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

colorizer = get_image_colorizer(artistic=True)

def colorize_image(source_path, render_factor=35):
    result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)
    return result_path
