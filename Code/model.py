# import torch
# from PIL import Image
# from torchvision import transforms
# from basicsr.models.archs.NAFNet_arch import NAFNet

# device = torch.device("cpu")

# # ------------------ MODEL LOADING ------------------ #
# def load_model(weight_path="denoising_model.pth"):
#     model = NAFNet(
#         img_channel=3,
#         width=64,
#         middle_blk_num=12,
#         enc_blk_nums=[2, 2, 4, 8],
#         dec_blk_nums=[2, 2, 2, 2]
#     )

#     checkpoint = torch.load(weight_path, map_location=device)

#     # Handle different checkpoint formats
#     if isinstance(checkpoint, dict):
#         if "params" in checkpoint:
#             model.load_state_dict(checkpoint["params"])
#         elif "state_dict" in checkpoint:
#             model.load_state_dict(checkpoint["state_dict"])
#         else:
#             model.load_state_dict(checkpoint)
#     else:
#         model.load_state_dict(checkpoint)

#     model.eval()
#     model.to(device)
#     return model


# model = load_model()

# # ------------------ TRANSFORM ------------------ #
# transform = transforms.ToTensor()

# # ------------------ INFERENCE ------------------ #
# def denoise_pil_image(pil_img: Image.Image) -> Image.Image:
#     # Force RGB (critical)
#     if pil_img.mode != "RGB":
#         pil_img = pil_img.convert("RGB")

#     img = transform(pil_img).unsqueeze(0).to(device)

#     with torch.no_grad():
#         output = model(img)

#     output = output.squeeze(0).clamp(0, 1).cpu()
#     output = transforms.ToPILImage()(output)

#     return output
import torch
from PIL import Image
from torchvision import transforms
from basicsr.models.archs.NAFNet_arch import NAFNet
from huggingface_hub import hf_hub_download

device = torch.device("cpu")

# ------------------ MODEL LOADING ------------------ #
def load_model():
    weight_path = hf_hub_download(
        repo_id="mouzanraza/image-denoiser",
        filename="denoising_model.pth"
    )

    model = NAFNet(
        img_channel=3,
        width=64,
        middle_blk_num=12,
        enc_blk_nums=[2, 2, 4, 8],
        dec_blk_nums=[2, 2, 2, 2]
    )

    checkpoint = torch.load(weight_path, map_location=device)

    if isinstance(checkpoint, dict):
        if "params" in checkpoint:
            model.load_state_dict(checkpoint["params"])
        elif "state_dict" in checkpoint:
            model.load_state_dict(checkpoint["state_dict"])
        else:
            model.load_state_dict(checkpoint)
    else:
        model.load_state_dict(checkpoint)

    model.eval()
    model.to(device)
    return model


# ------------------ TRANSFORM ------------------ #
transform = transforms.ToTensor()


# ------------------ INFERENCE ------------------ #
def denoise_pil_image(pil_img: Image.Image, model) -> Image.Image:
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")

    img = transform(pil_img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)

    output = output.squeeze(0).clamp(0, 1).cpu()
    output = transforms.ToPILImage()(output)

    return output
