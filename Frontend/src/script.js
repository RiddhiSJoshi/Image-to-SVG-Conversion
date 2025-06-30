async function uploadImage() {
  const fileInput = document.getElementById('imageUpload');
  const status = document.getElementById('status');
  const spinner = document.querySelector('.spinner');
  const svgContainer = document.getElementById('svgContainer');

  if (!fileInput.files.length) {
    status.textContent = "Please select at least one image.";
    return;
  }

  // Clear previous results
  svgContainer.innerHTML = "";
  status.textContent = "Converting...";
  spinner.style.display = "block";

  const file = fileInput.files[0];  // For now: handle only one image

  const query = `
    mutation($file: Upload!) {
      convertImageToSvg(file: $file) {
        svg
      }
    }
  `;

  const formData = new FormData();
  formData.append("operations", JSON.stringify({
    query: query,
    variables: { file: null }
  }));
  formData.append("map", JSON.stringify({ "0": ["variables.file"] }));
  formData.append("0", file, file.name);

  try {
    const response = await fetch("/graphql", {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    if (result.errors) {
      console.error(result.errors);
      status.textContent = "Error: " + result.errors[0].message;
    } else {
      const svg = result.data.convertImageToSvg.svg;

      // Create wrapper box
      const svgBox = document.createElement('div');
      svgBox.classList.add('svg-box');
      svgBox.innerHTML = svg;

      // Create download button
      const downloadBtn = document.createElement('a');
      downloadBtn.href = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
      downloadBtn.download = 'converted.svg';
      downloadBtn.className = 'download-btn';
      downloadBtn.textContent = 'Download SVG';

      svgBox.appendChild(downloadBtn);
      svgContainer.appendChild(svgBox);

      status.textContent = "Conversion complete ";
    }
  } catch (err) {
    console.error(err);
    status.textContent = "Something went wrong during upload.";
  }

  spinner.style.display = "none";
}
