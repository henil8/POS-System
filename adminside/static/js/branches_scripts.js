// Another new code

// Toggle search input on small devices
function toggleSearch() {
  let searchContainer = document.querySelector(".search-container");
  let searchInput = document.querySelector(".search-input");

  searchContainer.classList.toggle("active");
  if (searchContainer.classList.contains("active")) {
    searchInput.focus();
  }
}

// Search function
// document.getElementById("searchInput").addEventListener("keyup", function () {
//   let filter = this.value.toLowerCase();
//   let rows = document.querySelectorAll("#storeTableBody tr");

//   rows.forEach(function (row) {
//     let store = row.cells[1].textContent.toLowerCase();
//     let manager = row.cells[2].textContent.toLowerCase();

//     if (store.includes(filter) || manager.includes(filter)) {
//       row.style.display = "";
//     } else {
//       row.style.display = "none";
//     }
//   });
// });

let ID = 1;
let updateIndex = null; // Stores the row reference for update

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("storeForm").addEventListener("submit", function (event) {
      event.preventDefault();
      if (validateForm()) {
       
        document.getElementById("storeForm").submit();
      }
    });
    document.getElementById("formUpdate").addEventListener("submit", function (event) {
      event.preventDefault();
      if (validateUpdateForm()) {
        document.getElementById("formUpdate").submit();
      } 
    });

    document.getElementById("FormDelete").addEventListener("submit", function (event) {
      
      
        document.getElementById("FormDelete").submit();
      
    });

  populateStaticDropdowns();
});

function populateStaticDropdowns() {
  let statuss = ["Open", "Close"];
  let statusDropdown = document.getElementById("status");
  if (statusDropdown.options.length === 1) {
  statuss.forEach((status) => {
    let option = document.createElement("option");
    option.value = status;//1,2,3
    option.textContent = status;
    statusDropdown.appendChild(option);
  });
}
}


function validateForm() {
  let phoneNo = document.getElementById("PhoneNo");
  let status = document.getElementById("status");

  let phoneNoValue = phoneNo.value.trim();
  let statusValue = status.value.trim();

  let phoneNoRegex = /^(?:\+91[-\s]?)?[6-9]\d{9}$/;

  removeError(phoneNo);
  removeError(status);
  clearErrors();

  let isValid = true;

  if (!phoneNoRegex.test(phoneNoValue)) {
    showError(
      phoneNo,
      "Invalid Phone Format. Phone number must be 10 digits & start with 6-9 (e.g., 9876543210)"
    );
    isValid = false;
  }

  if (!statusValue) {
    showError(status, "Status is required");
    isValid = false;
  }

  return isValid;
}

function validateUpdateForm() {
  let phoneNo = document.getElementById("updatePhoneNo");
  let status = document.getElementById("updateStatus");

  let phoneNoValue = phoneNo.value.trim();
  let statusValue = status.value.trim();

  let phoneNoRegex = /^(?:\+91[-\s]?)?[6-9]\d{9}$/;

  removeError(phoneNo);
  removeError(status);
  clearErrors();

  let isValid = true;

  if (!phoneNoRegex.test(phoneNoValue)) {
      showError(
          phoneNo,
          "Invalid Phone Format. Phone number must be 10 digits & start with 6-9 (e.g., 9876543210)"
      );
      isValid = false;
  }

  if (!statusValue) {
      showError(status, "Status is required");
      isValid = false;
  }

  return isValid;
}

function showError(input, message) {
  let errorSpan = document.createElement("span");
  errorSpan.classList.add("error-message");
  errorSpan.style.color = "red";
  errorSpan.style.fontSize = "12px";
  errorSpan.innerText = message;
  input.parentNode.appendChild(errorSpan);
}

function removeError(input) {
  let error = input.parentNode.querySelector(".error-message");
  if (error) {
    error.remove();
  }
}

function addBranch() {
  let location = document.getElementById("location").value.trim();
  let area = document.getElementById("storeArea").value.trim();
  let manager = document.getElementById("managerID").value.trim();
  let phoneNo = document.getElementById("PhoneNo").value.trim();
  let status = document.getElementById("status").value;

  let newRow = document.createElement("tr");
  newRow.innerHTML = `
        <td>${ID}</td>
        <td>${location}</td>
        <td>${area}</td>
        <td>${manager}</td>
        <td>${phoneNo}</td>
        <td>${status}</td>
        <td class="action-buttons">
            <button class="update-btn" onclick="updateRow(this)"><i class="fas fa-edit"></i></button>
            <button class="delete-btn" onclick="deleteRow(this)"><i class="fas fa-trash"></i></button>
        </td>
    `;

  document.getElementById("storeTableBody").appendChild(newRow);
  ID++;
  document.getElementById("storeForm").reset();
  closeForm();
}

function clearErrors() {
  document.querySelectorAll(".error-message").forEach((el) => {
    el.textContent = "";
  });
}

function updateRow(button) {
  let row = button.closest("tr");
  let columns = row.getElementsByTagName("td");

  document.getElementById("location").value = columns[1].textContent;
  document.getElementById("storeArea").value = columns[2].textContent;
  document.getElementById("managerID").value = columns[3].textContent;
  document.getElementById("PhoneNo").value = columns[4].textContent;
  document.getElementById("status").value = columns[5].textContent;

  updateIndex = row; // Store reference to the row for updating
  openForm(true);
}

function saveUpdatedBranch() {  
  if (updateIndex) {
    let location = document.getElementById("location").value;
    let area = document.getElementById("storeArea").value;
    let manager = document.getElementById("managerID").value;
    let phoneNo = document.getElementById("PhoneNo").value;
    let status = document.getElementById("status").value;

    updateIndex.cells[1].textContent = location;
    updateIndex.cells[2].textContent = area;
    updateIndex.cells[3].textContent = manager;
    updateIndex.cells[4].textContent = phoneNo;
    updateIndex.cells[5].textContent = status;

    updateIndex = null; // Reset after update
    document.getElementById("storeForm").reset();
    closeForm();
  }
}

function deleteRow(button) {
  button.closest("tr").remove();
}




function openUpdateForm(id, location, area, managerID, phoneNo, status) {
  document.getElementById("branchID").value = id;
  document.getElementById("updateLocation").value = location;
  document.getElementById("updateArea").value = area;
  document.getElementById("updateManagerID").value = managerID;
  document.getElementById("updatePhoneNo").value = phoneNo;
  document.getElementById("updateStatus").value = status;

  document.getElementById("updateOverlay").style.display = "block";
  document.getElementById("updateForm").style.display = "block";
}

function closeUpdateForm() {
  document.getElementById("updateOverlay").style.display = "none";
  document.getElementById("updateForm").style.display = "none";
}
 
function sureform(id){
  console.log("Setting bID to:", id);
  document.getElementById("bID").value = id;

  document.getElementById("deleteOverlay").style.display = "block";
  document.getElementById("deleteForm").style.display = "block";
}

function  closedeleteForm(){
  document.getElementById("deleteOverlay").style.display = "none";
  document.getElementById("deleteForm").style.display = "none";
}

function openForm(isUpdate = false) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  if (!isUpdate) {
    resetForm(); // Clears the form ONLY when adding a new chain
    updateIndex = null; // Clear any previous update reference
  }
}
function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");

  resetForm();
  updateIndex = null; // Reset update index when closing the form
}

function resetForm() {
  document.getElementById("storeForm").reset(); // Resets all input fields
}
