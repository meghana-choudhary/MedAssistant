document
  .getElementById("diabetesForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const result = document.getElementById("result");
    result.style.display = "block";
    result.innerHTML = "Processing..."; 

    try {
      const response = await fetch("/predict_diabetes", {
        method: "POST",
        body: new FormData(this),
      });

      const responseText = await response.text();
      console.log("Raw response:", responseText);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = JSON.parse(responseText); 
      result.innerHTML = data.result || "No result returned";
    } catch (error) {
      console.error("Full error:", error);
      result.innerHTML = `
            Error: ${error.message}<br>
            Check console for details
        `;
    }
  });
