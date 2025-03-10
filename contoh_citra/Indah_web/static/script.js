document.getElementById("imageInput").addEventListener("change", (event) => {
    const preview = document.getElementById("preview");
    const [file] = event.target.files;

    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});
