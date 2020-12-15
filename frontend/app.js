document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("speech-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      let file = document.getElementById("form-file").files[0];
      if (file) {
        document.getElementById(
          "results"
        ).innerHTML = `<p class='loading'>Predicting Class....</p>`;
        let formData = new FormData();
        formData.append("image", file);
        fetch("http://127.0.0.1:5000/file", {
          method: "POST",
          body: formData,
        })
          .then((res) => res.json())
          .then((result) => {
            let ele = document.getElementById("results");
            let type =
              result.result[2] === "D"
                ? "Dysarthric Speech"
                : "Non Dysarthric Speech";
            ele.innerHTML = `
            <h3> Results </h3>
            <p><b>Time 🕒 : </b>
            
            ${result.time}</p>
            <p><b>Class : </b> ${type}</p>`;
            return;
          });
      }
    });
});
