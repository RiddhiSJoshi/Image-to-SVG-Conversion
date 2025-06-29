const uploadInput = document.getElementById('imageUpload');
const statusEl = document.getElementById('status');
const svgContainer = document.getElementById('svgContainer');

uploadInput.addEventListener('change', async (event) => {
  const files = event.target.files;

  if (!files.length) {
    return;
  }

  statusEl.innerHTML = `
    <div class="spinner"></div>
    <p>Converting ${files.length} file(s)...</p>
  `;

  svgContainer.innerHTML = '';

  // Simulate conversion delay
  // await sleep(2000);

  for (const file of files) {
    const svgString = await convertImageToSvg(file);
    renderSvg(svgString, file.name);
  }

  statusEl.textContent = 'Conversion complete!';
});

async function convertImageToSvg(file) {
  const query = `
    mutation ConvertImage($file: Upload!) {
      convertImageToSvg(file: $file) {
        svg
      }
    }
  `;

  const operations = JSON.stringify({
    query,
    variables: {
      file: null // placeholder for file
    }
  });

  const map = JSON.stringify({
    "0": ["variables.file"]
  });

  const formData = new FormData();
  formData.append("operations", operations);
  formData.append("map", map);
  formData.append("0", file, file.name);

  try {
    const response = await fetch("/graphql", {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    console.log("GraphQL response:", result);

    const svg = result?.data?.convertImageToSvg?.svg;

    if (!svg) {
      throw new Error("No SVG returned from server.");
    }

    return svg;
  } catch (err) {
    console.error(err);
    return `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
      <rect width="200" height="200" fill="red"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="16" fill="#fff">
        ERROR
      </text>
    </svg>`;
  }
}


function renderSvg(svgString, filename) {
  const div = document.createElement('div');
  div.className = 'svg-box';

  div.innerHTML = `
    ${svgString}
    <a class="download-btn" href="data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgString)}" download="${filename.replace(/\.\w+$/, '.svg')}">
      Download SVG
    </a>
  `;

  svgContainer.appendChild(div);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function randomHexColor() {
  return Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
}
