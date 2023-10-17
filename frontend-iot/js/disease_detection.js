const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.querySelector(".upload-file");
const button = document.getElementById("detect-disease-btn");
const imageName = document.getElementById("image-name");

inputFile.addEventListener("change", uploadImageHandler);

function uploadImageHandler() {
    let imgLink = URL.createObjectURL(inputFile.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.style.border = 0;
    imageView.textContent = "";
    button.classList.remove("display-none");
    imageName.innerText = inputFile.files[0].name;
}

dropArea.addEventListener("dragover", (event) => {
    event.preventDefault();
    imageView.classList.add("image-view-on-drag");
    imageView.classList.remove("ajax-upload-dragdrop");
});

dropArea.addEventListener("dragleave", (event) => {
    event.preventDefault();
    imageView.classList.remove("image-view-on-drag");
    imageView.classList.add("ajax-upload-dragdrop");
});

dropArea.addEventListener("drop", (event) => {
    event.preventDefault();
    inputFile.files = event.dataTransfer.files;
    imageView.classList.remove("image-view-on-drag");
    imageView.classList.add("ajax-upload-dragdrop");
    uploadImageHandler();
});