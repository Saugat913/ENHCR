
const fileInput = document.getElementById('file-input');
const button = document.getElementById('button');
const errorMessage = document.getElementById('error-message');
const container = document.getElementById('container');

const imageContainer = document.getElementById('image-container');
const previewImage = document.getElementById('file-image');
const resultImage = document.getElementById('result-image');


const fileTitle = document.querySelector(".title");




button.addEventListener('click', () => {
    errorMessage.style.display = 'none';
    fileInput.click();
});

fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    const allowedExtensions = ['jpeg', 'jpg'];



    function displayError(message, timeout = 3000) { // Set default timeout if needed
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, timeout);
    }




    const extension = file.name.split('.').pop().toLowerCase();




    console.log(extension);

    if (!allowedExtensions.includes(extension)) {
        event.target.value = ''; // Clear file selection
        displayError('Invalid file format. Please upload a JPG or JPEG image.')
    } else {


        const reader = new FileReader();



        reader.onload = function (event) {


            previewImage.src = event.target.result;
            imageContainer.style.display = 'flex';

        };

        reader.readAsDataURL(file); // Read the file and convert it to a data URL


        // Send the file to the server using Fetch API
        try {
            const formData = new FormData();
            formData.append('file-input', file);



            button.textContent = 'Processing....';
            fileTitle.textContent = file.name;



            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error uploading file: ${response.statusText}`);
            }





            let url = URL.createObjectURL(await response.blob());

            resultImage.src = url;

            // Handle successful upload response (e.g., display message)
            console.log('File uploaded successfully!');
          
        } catch (error) {
            errorMessage.textContent = `Error uploading file: ${error.message}`;
        } finally {
            // Hide progress message (optional)
            button.textContent = 'Choose file';
        }
        errorMessage.style.display = 'none'; // Hide the error message
    }
});