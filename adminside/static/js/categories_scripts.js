let currentRow = null; 
let categoryId = 1; 

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("foodItemForm").addEventListener("submit", function (event) {
        event.preventDefault();
        if (validateForm()) {
            console.log("Form is valid. Submitting...");
            this.submit();  // Ensures form submission
        } else {
            console.log("Form validation failed!");
        }
        });
    
    document.getElementById("formUpdate").addEventListener("submit", function (event) {
        event.preventDefault();
        if (validateUpdateForm()) {
            console.log("Form is valid. Submitting...");
            this.submit();  // Ensures form submission
        } else {
            console.log("Form validation failed!");
        }
        });
    
    populateStaticDropdowns()
});


function toggleSearch() {
    let searchContainer = document.querySelector(".search-container");
    let searchInput = document.querySelector(".search-input");
    
    searchContainer.classList.toggle("active");
    if (searchContainer.classList.contains("active")) {
        searchInput.focus();
    }
}

// Search function
document.getElementById("searchInput").addEventListener("keyup", function () {
    let filter = this.value.trim().toLowerCase();
    let rows = document.querySelectorAll("#foodTableBody tr");
    
    rows.forEach(function (row) {
        let itemname = row.cells[1].textContent.trim().toLowerCase();
        if (itemname.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});


function populateStaticDropdowns() {
    let statuss = ["Available", "Not Available"];
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

    let status = document.getElementById("status");
    let item_name=document.getElementById("itemName");
 
    let statusValue = status.value.trim();
    let item_nameValue=item_name.value.trim();
  
    removeError(status);
    removeError(item_name);
    clearErrors();
  
    let isValid = true;
    
    if (!item_nameValue) {
        showError(item_name, "Category Name is required");
        isValid = false;
    }
   
  
    if (!statusValue) {
      showError(status, "Status is required");
      isValid = false;
    }
  
    return isValid;
  }
  function validateUpdateForm() {

    let status = document.getElementById("updatestatus");
    let item_name=document.getElementById("updateitemName");
 
    let statusValue = status.value.trim();
    let item_nameValue=item_name.value.trim();
  
    removeError(status);
    removeError(item_name);
    clearErrors();
  
    let isValid = true;
    
    if (!item_nameValue) {
        showError(item_name, "Category Name is required");
        isValid = false;
    }
   
  
    if (!statusValue) {
      showError(status, "Status is required");
      isValid = false;
    }
  
    return isValid;
  }
  
function removeError(input) {
    let error = input.parentNode.querySelector(".error-message");
    if (error) {
      error.remove();
    }
  }

function showError(input, message) {
    let errorSpan = document.createElement("span");
    errorSpan.classList.add("error-message");
    errorSpan.style.color = "red";
    errorSpan.style.fontSize = "12px";
    errorSpan.innerText = message;
    input.parentNode.appendChild(errorSpan);
}

function clearErrors() {
    document.querySelectorAll(".error-message").forEach((el) => {
      el.textContent = "";
    });
  }

// Function to add or update a category
function saveCategory() {
    let itemName = document.getElementById("itemName").value.trim();
    let nameError = document.getElementById("nameError");
    
    nameError.textContent = "";
    if (!itemName) {
        nameError.textContent = "Category name is required.";
        return;
    }
    
    if (currentRow) {
        // If updating an existing row
        currentRow.cells[1].innerText = itemName;
    } else {
        // Creating a new row
        let newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${categoryId}</td>
            <td>${itemName}</td>
            <td>
                <label class="switch">
                    <input type="checkbox" onclick="toggleStatus(this)" checked>
                    <span class="slider round"></span>
                </label>
            </td>
            <td>
                <button class="update-btn" onclick="updateRow(this)">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="delete-btn" onclick="deleteRow(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        document.getElementById("foodTableBody").appendChild(newRow);
        categoryId++;
    }
    
    document.getElementById("foodItemForm").reset(); 
    closeForm();
    currentRow = null;
}

// Function to toggle category status
function toggleStatus(checkbox) {
    if (checkbox.checked) {
        console.log("Status: ON");
    } else {
        console.log("Status: OFF");
    }
}

function resetForm() {
    document.getElementById("foodItemForm").reset(); // Resets all input fields
}

// Function to handle updating a category
function updateRow(button) {
    currentRow = button.closest("tr");
    let name = currentRow.cells[1].innerText;
    document.getElementById("itemName").value = name;
    openForm(true);
}

// Function to delete a category row
function deleteRow(button) {
    button.closest("tr").remove();
}

// Open form modal
// function openForm() {
//     document.getElementById("overlay").style.display = "block";
//     document.getElementById("myForm").style.display = "block";
//     document.body.classList.add("popup-open");
// }
function openForm(isUpdate = false) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("myForm").style.display = "block";
    document.body.classList.add("popup-open");
  
    if (!isUpdate) {
        resetForm();  // Clears the form ONLY when adding a new chain
        updateIndex = null; // Clear any previous update reference
    }
}
// Close form modal
function closeForm() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("myForm").style.display = "none";
    document.body.classList.remove("popup-open");
   
    // Reset currentRow to prevent unintended deletions
    currentRow = null;
}
function openUpdateForm(id,name,status) {
    document.getElementById("updateitemID").value = id;
    // document.getElementById("updateitemIDDisplay").value = id;  
    document.getElementById("updateitemName").value = name;
    document.getElementById("updatestatus").value = status;
  
    document.getElementById("updateOverlay").style.display = "block";
    document.getElementById("updateForm").style.display = "block";
  }
  
  function closeUpdateForm() {
    document.getElementById("updateOverlay").style.display = "none";
    document.getElementById("updateForm").style.display = "none";
  }
   
  function sureform(id){
    console.log("Setting bID to:", id);
    document.getElementById("iID").value = id;
  
    document.getElementById("deleteOverlay").style.display = "block";
    document.getElementById("deleteForm").style.display = "block";
  }
  
  function  closedeleteForm(){
    document.getElementById("deleteOverlay").style.display = "none";
    document.getElementById("deleteForm").style.display = "none";
  }