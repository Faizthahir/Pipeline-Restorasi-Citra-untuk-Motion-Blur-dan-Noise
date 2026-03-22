import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
import time

def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = img.astype(np.float32)
    return img

def motion_psf(length=15, angle=30):
    psf = np.zeros((length, length))
    center = length // 2

    for i in range(length):
        x = int(center + (i - center) * np.cos(np.deg2rad(angle)))
        y = int(center + (i - center) * np.sin(np.deg2rad(angle)))
        if 0 <= x < length and 0 <= y < length:
            psf[y, x] = 1

    psf /= psf.sum()
    return psf

def add_motion_blur(img, psf):
    return convolve2d(img, psf, mode='same', boundary='wrap')

def add_gaussian_noise(img, sigma=20):
    noise = np.random.normal(0, sigma, img.shape)
    return np.clip(img + noise, 0, 255)

def add_salt_pepper(img, prob=0.05):
    noisy = img.copy()
    rnd = np.random.rand(*img.shape)

    noisy[rnd < prob/2] = 0
    noisy[rnd > 1 - prob/2] = 255

    return noisy

def inverse_filter(img, psf, eps=1e-3):
    img_fft = np.fft.fft2(img)
    psf_fft = np.fft.fft2(psf, s=img.shape)

    result_fft = img_fft / (psf_fft + eps)
    result = np.abs(np.fft.ifft2(result_fft))

    return np.clip(result, 0, 255)

def wiener_filter(img, psf, K=0.01):
    img_fft = np.fft.fft2(img)
    psf_fft = np.fft.fft2(psf, s=img.shape)
    psf_conj = np.conj(psf_fft)

    result_fft = (psf_conj / (np.abs(psf_fft)**2 + K)) * img_fft
    result = np.abs(np.fft.ifft2(result_fft))

    return np.clip(result, 0, 255)

def lucy_richardson(img, psf, iterations=10):
    img = img / 255.0
    estimate = np.full(img.shape, 0.5)

    psf_mirror = np.flip(psf)

    for _ in range(iterations):
        conv = convolve2d(estimate, psf, mode='same')
        relative_blur = img / (conv + 1e-5)
        estimate *= convolve2d(relative_blur, psf_mirror, mode='same')

    return np.clip(estimate * 255, 0, 255)

def evaluate(original, restored):
    mse_val = np.mean((original - restored) ** 2)
    psnr_val = psnr(original, restored, data_range=255)
    ssim_val = ssim(original, restored, data_range=255)

    return mse_val, psnr_val, ssim_val

if __name__ == "__main__":
    img = load_image("D:\\Semester 4\\Pengolahan Citra Digital\\Minggu 6\\input.jpeg")

    psf = motion_psf(length=15, angle=30)

    # Degradasi
    blur = add_motion_blur(img, psf)
    gauss_blur = add_gaussian_noise(blur, sigma=20)
    sp_blur = add_salt_pepper(blur, prob=0.05)

    results = {}

    for name, degraded in {
        "Motion Blur": blur,
        "Gaussian + Blur": gauss_blur,
        "SaltPepper + Blur": sp_blur
    }.items():

        print(f"\n=== {name} ===")

        # Inverse
        start = time.time()
        inv = inverse_filter(degraded, psf)
        t_inv = time.time() - start

        # Wiener
        start = time.time()
        wien = wiener_filter(degraded, psf, K=0.01)
        t_wien = time.time() - start

        # Lucy-Richardson
        start = time.time()
        lr = lucy_richardson(degraded, psf, iterations=10)
        t_lr = time.time() - start

        # Evaluasi
        results[name] = {
            "Inverse": (*evaluate(img, inv), t_inv),
            "Wiener": (*evaluate(img, wien), t_wien),
            "Lucy-Richardson": (*evaluate(img, lr), t_lr)
        }

        print("Inverse:", results[name]["Inverse"])
        print("Wiener:", results[name]["Wiener"])
        print("Lucy:", results[name]["Lucy-Richardson"])

    plt.figure(figsize=(12,8))
    plt.subplot(2,2,1); plt.imshow(img, cmap='gray'); plt.title("Original")
    plt.subplot(2,2,2); plt.imshow(blur, cmap='gray'); plt.title("Motion Blur")
    plt.subplot(2,2,3); plt.imshow(gauss_blur, cmap='gray'); plt.title("Gaussian + Blur")
    plt.subplot(2,2,4); plt.imshow(sp_blur, cmap='gray'); plt.title("Salt & Pepper + Blur")
    plt.show()