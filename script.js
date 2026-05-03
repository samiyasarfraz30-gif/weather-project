// function uploadImage() {
//     const fileInput = document.getElementById("imageInput");
//     const file = fileInput.files[0];

//     if (!file) {
//         alert("Please select an image");
//         return;
//     }

//     // Show preview
//     const preview = document.getElementById("preview");
//     preview.innerHTML = `<img src="${URL.createObjectURL(file)}">`;

//     const formData = new FormData();
//     formData.append("file", file);

//     fetch("http://127.0.0.1:5000/predict", {
//         method: "POST",
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {

//     console.log("Backend Response:", data);

//     if (data.error) {
//         document.getElementById("result").innerText = "Error: " + data.error;
//         return;
//     }

//     document.getElementById("result").innerText =
//         "Prediction: " + data.prediction;

//     document.getElementById("time").innerHTML =
//         "Serial Time: " + data.serial_time.toFixed(4) +
//         " sec <br> Parallel Time: " + data.parallel_time.toFixed(4) + " sec";
// })
//     .catch(error => {
//         console.error(error);
//         alert("Error connecting to backend");
//     });
// }













let selectedFile = null;

document.getElementById('uploadZone').addEventListener('click', function() {
    document.getElementById('imageInput').click();
});

document.getElementById('imageInput').addEventListener('change', function() {
    if (!this.files[0]) return;
    selectedFile = this.files[0];
    
    let reader = new FileReader();
    reader.onload = function(e) {
        let img = document.getElementById('preview');
        img.src = e.target.result;
        img.style.display = 'block';
        document.getElementById('uploadZone').style.display = 'none';
    };
    reader.readAsDataURL(selectedFile);
});

document.getElementById('predictBtn').addEventListener('click', function() {
    if (!selectedFile) { alert('Please select an image first!'); return; }

    document.getElementById('predictBtn').disabled = true;
    document.getElementById('loader').style.display = 'block';
    document.getElementById('resultBox').style.display = 'none';

    let formData = new FormData();
    formData.append('file', selectedFile);

    fetch('http://127.0.0.1:5000/predict', { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('predictBtn').disabled = false;
            document.getElementById('resultBox').style.display = 'block';

            if (data.error) {
                document.getElementById('resultText').innerText = 'Error: ' + data.error;
                return;
            }
            document.getElementById('resultText').innerText = data.prediction;
            document.getElementById('serialTime').innerText = parseFloat(data.serial_time).toFixed(4) + ' sec';
            document.getElementById('parallelTime').innerText = parseFloat(data.parallel_time).toFixed(4) + ' sec';
        })
        .catch(err => {
            document.getElementById('loader').style.display = 'none';
            document.getElementById('predictBtn').disabled = false;
            console.error('ERROR:', err);
        });
});