function toggleSubMenu(id) {
    var subMenu = document.getElementById(id);
    if (subMenu.style.display === "none") {
        subMenu.style.display = "block";
    } else {
        subMenu.style.display = "none";
    }
}

// async function uploadFile(event) {
//     event.preventDefault();
//     let formData = new FormData(event.target);
//     let response = await fetch("/upload", {
//         method: "POST",
//         body: formData,
//     });

//     if (response.ok) {
//         let result = await response.text();
//         document.getElementById("dataframe-display").innerHTML = result;
//     } else {
//         alert("File upload failed.");
//     }
// }

async function uploadFile(event) {
    event.preventDefault();
    let formData = new FormData(event.target);
    let response = await fetch("/upload", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        let result = await response.text();
        document.getElementById("dataframe-display").innerHTML = result;
    } else {
        let errorText = await response.text();
        alert(`File upload failed: ${errorText}`);
    }
}