const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");
const resultDiv = document.getElementById("result");

imageInput.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      previewContainer.style.display = "block";
    };
    reader.readAsDataURL(file);
  }
});

async function analyzeImage() {
  const file = imageInput.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  resultDiv.innerHTML = "Analyzing...";
  resultDiv.style.display = "block";

  try {
    const response = await fetch("/predict_pneumonia", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    resultDiv.innerHTML = `<strong>Result:</strong> ${data.result}`;
  } catch (error) {
    console.error("Error:", error);
    resultDiv.innerHTML = "An error occurred. See console for details.";
  }
}
