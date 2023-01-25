let progress = document.querySelector('#progress');
let progress_wrapper = document.querySelector('#progress_wrapper');
let progress_status = document.querySelector('#progress_status');

let upload_btn = document.querySelector('#upload_btn');
let loading_btn = document.querySelector('#loading_btn');
let cancel_btn = document.querySelector('#cancel_btn');

let alert_wrapper = document.querySelector('#alert_wrapper');

let input = document.querySelector('#file_input');
let file_input_label = document.querySelector('#file_input_label');
let file_table = document.querySelector('.filesTable')

function show_alert(message, alert) {
  alert_wrapper.innerHTML = `
      <div class="alert alert-${alert} alert-dismissible fade show" role="alert">
        <span>${message}</span>
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
        </div>
    `;
}

function input_filename() {
  file_input_label.innerText = input.files[0].name;
}

function upload(url) {
  if (!input.value) {
    show_alert("No file selected", "warning");
    return;
  }

  let data = new FormData();

  let request = new XMLHttpRequest();
  request.responseType = `json`;

  alert_wrapper.innerHTML = "";
  input.disabled = true;

  upload_btn.classList.add('d-none');

  loading_btn.classList.remove("d-none");

  cancel_btn.classList.remove("d-none");

  progress_wrapper.classList.remove("d-none");

  let file = input.files[0];
  let filename = file.name;
  let filesize = file.size;

  data.append("file", file);

  request.upload.addEventListener("progress", function (e) {
    let loaded = e.loaded;
    let total = e.total;

    let percentage_complete = (loaded / total) * 100;

    progress.setAttribute("style", `width: ${Math.floor(percentage_complete)}%`);
    progress_status.innerText = `${Math.floor(percentage_complete)}% uploaded`;

  });

  request.addEventListener("load", function (e) {
    if (request.status == 200) {
      show_alert(`${request.response.message}`, 'success');
      let table = document.querySelector(".filesTable");
      let count_folders = document.querySelectorAll('tr');

      let new_row = document.createElement('tr');
      new_row.id = count_folders.length

      new_row.innerHTML = `<th scope="row">${count_folders.length}</th>
      <td>${filename}</td>
      <td>${filesize} байт</td>
      <td>
      <button onclick="delete_file('delete-file/', '${count_folders.length}', '${request.response.folderId}');" class="btn btn-danger">Видалити</button>
  </td>
      `
      table.append(new_row)
    
    }
    else {
      console.log(e)
      show_alert("Error uploading file", "danger");
    }

    reset();

  });

  request.addEventListener("error", function (e) {

    reset();
    console.log(e)
    show_alert("Error uploading file", "danger");

  });

  request.open("post", url);
  request.send(data);

  cancel_btn.addEventListener("click", function () {
    request.abort();
  });

}
function reset() {
  input.value = null;

  input.disabled = false;

  cancel_btn.classList.add("d-none");

  loading_btn.classList.add("d-none");

  upload_btn.classList.remove("d-none");

  progress_wrapper.classList.add("d-none");

  progress.setAttribute("style", "width: 0%");

  file_input_label.innerText = "Select file";
}

function delete_file(url, id,folderId){
  try {
    let row = document.getElementById(`${id}`);
    row.remove();
    let request = new XMLHttpRequest();
    let data = new FormData();

    request.responseType = `json`

    request.addEventListener("load", function (e) {
        if (request.status == 200) {
            show_alert(`${request.response.message}`, 'success');
        }
    });

   request.addEventListener("error", function (e) {

    console.log(e)
    show_alert("Error uploading file", "danger");

  });

    request.open("post", url+folderId);
    request.send(data)

  } catch (error) {
    console.log(error)
  }
}