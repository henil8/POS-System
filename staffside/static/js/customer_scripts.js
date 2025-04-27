// Toggle search input on small devices
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");

  if (searchInput) {
    searchInput.addEventListener("keyup", function () {
      let filter = this.value.toLowerCase();
      let rows = document.querySelectorAll("#customerBody tr");

      rows.forEach(function (row) {
        let name = row.cells[0]?.textContent.toLowerCase() || "";
        let phone = row.cells[1]?.textContent.toLowerCase() || "";
        if (name.includes(filter) || phone.includes(filter)) {
          row.style.display = "";
        } else {
          row.style.display = "none";
        }
      });
    });
  }
});

// Toggle search input visibility on small devices

function openUpdateForm(id, name,phone_no,email) {

  document.getElementById("update_id").value = id;
  document.getElementById("update_name").value = name;
  document.getElementById("update_phone_no").value = phone_no;
  document.getElementById("update_email").value = email;


  document.getElementById("overlay-update").style.display = "block";
  document.getElementById("updateFormPopup").style.display = "block";
}

function closeUpdateForm() {
  document.getElementById("overlay-update").style.display = "none";
  document.getElementById("updateFormPopup").style.display = "none";
}

function openForm() {
  document.getElementById("purchaseForm").reset();
  document.getElementById("myForm").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}
function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");
    
  // Reset update index when closing the form
}

function openDeleteForm(id) {
  document.getElementById("delete_id").value = id;
  document.getElementById("overlay-delete").style.display = "block";
  document.getElementById("deleteFormPopup").style.display = "block";
}

function closeDeleteForm() {
  document.getElementById("overlay-delete").style.display = "none";
  document.getElementById("deleteFormPopup").style.display = "none";
}
