# AI Image Denoiser

- **Student Name**: Zain Ul abadn
- **Roll Number**: 100052
- **Course Name**: Digital Image Processing
- **Project Description**: 
  A premium, production-ready web application for AI-powered image denoising using the state-of-the-art NAFNet architecture.
  Transform noisy images into high-quality outputs with cutting-edge deep learning technology.
  The project utilizes NAFNet for efficient and effective image restoration.
  It includes a web interface for easy interaction and testing of the model.

- **Objectives**:
  - To implement an AI-based image denoising system using NAFNet.
  - To develop a responsive web interface for easy user interaction.
  - To evaluate the varying noise levels and restoration quality.
  - To understand the practical applications of Deep Learning in Image Processing.

- **Tools & Technologies Used**: 
  - Python
  - PyTorch
  - FastAPI
  - NAFNet (Neural Architecture for Noise Reduction)
  - BasicSR
  - HTML/CSS/JavaScript

- **Steps to Run the Code**:
  1. **Install Dependencies**:
     Navigate to the project directory and run:
     ```bash
     pip install -r Code/supporting_files/requirements.txt
     ```
  2. **Run the Notebook**:
     Open `Code/Colab_code.ipynb` in Jupyter Notebook or Google Colab. Ensure the kernel is set to the correct environment.
     Note: You may need to adjust `sys.path` to include `Code/supporting_files` if imports fail.
  3. **Run the Web Application (Optional)**:
     ```bash
     cd Code/supporting_files
     python -m uvicorn api.index:app --reload
     ```

- **Sample Input and Output Images**:
  
  | Input (Noisy) | Output (Denoised) |
  | :---: | :---: |
  | ![Input](Dataset/testing_photos/Dataset/testing_photos/Input_image/1.jpg) | ![Output](Dataset/testing_photos/Results/output_images/1.png) |

  *(See `Results/output_images` and `Dataset` folder for more examples)*

- **Conclusion**:
  This project successfully implements a state-of-the-art image denoising solution using NAFNet. The model demonstrates superior performance in recovering fine details from noisy images. The accompanying web application makes this advanced technology accessible and easy to use.

