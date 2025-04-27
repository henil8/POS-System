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
document.getElementById("searchInput").addEventListener("keyup", function () {
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll("#supplierTableBody tr");
 
    rows.forEach(function (row) {
        let name = row.cells[1].textContent.toLowerCase();
        let company = row.cells[2].textContent.toLowerCase();
 
        if (name.includes(filter) || company.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});
 
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("supplierForm").addEventListener("submit", function (event) {
        event.preventDefault();
        if (validateForm()) {
            document.getElementById("supplierForm").submit();
          }
    });
   
    document.addEventListener("DOMContentLoaded", function () {
        const updateForm = document.getElementById("formUpdate");
    
        updateForm.addEventListener("submit", function (event) {
            if (!validateUpdateForm()) {
                event.preventDefault(); // only prevent if invalid
            }
        });
    });

});
 

 
 
function validateForm() {
    let isValid = true;
    clearErrors();
 
    function showError(input, message) {
        let errorSpan = document.getElementById(input.id + "Error");
        errorSpan.textContent = message;
        errorSpan.style.color = "red";
    }
 
    let name = document.getElementById("supplierName");
    let company = document.getElementById("companyName");
    let email = document.getElementById("supplierEmail");
    let address = document.getElementById("supplierAddress");
    let phone = document.getElementById("supplierPhone");
    let store = document.getElementById("supplierStore");
 
    if (!name.value.trim()) {
        showError(name, "Name is required");
        isValid = false;
    }
    if (!company.value.trim()) {
        showError(company, "Company Name is required");
        isValid = false;
    }
    if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, "Enter a valid email");
        isValid = false;
    }
    if (!address.value.trim()) {
        showError(address, "Address is required");
        isValid = false;
    }
    if (!phone.value.trim() || !/^[6789]\d{9}$/.test(phone.value)) {
        showError(phone, "Enter a valid 10-digit phone number starting with 6,7,8,9");
        isValid = false;
    }
    if (!store.value.trim()) {
        showError(store, "Please select a store");
        isValid = false;
    }
    return isValid;
}
 
function clearErrors() {
    let errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach(error => error.textContent = "");
}
 
function openForm(isUpdate = false) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("myForm").style.display = "block";
    document.body.classList.add("popup-open");
    if (!isUpdate) {
        document.getElementById("supplierForm").reset();
        updateIndex = null;
    }
}
 
function closeForm() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("myForm").style.display = "none";
    document.body.classList.remove("popup-open");
    updateIndex = null;
}
 

function removeError(input) {
  let error = input.parentNode.querySelector(".error-message");
  if (error) {
    error.remove();
  }
}
function clearErrors() {
    let errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach(error => error.textContent = "");
}
 
function validateUpdateForm() {
    let isValid = true;
    clearErrors();

    function showError(input, message) {
        let errorSpan = document.createElement("span");
        errorSpan.classList.add("error-message");
        errorSpan.style.color = "red";
        errorSpan.textContent = message;
        input.parentNode.appendChild(errorSpan);
    }

    let name = document.getElementById("updateName");
    let email = document.getElementById("updateEmail");
    let phone = document.getElementById("updatePhone");

    if (!name.value.trim()) {
        showError(name, "Name is required");
        isValid = false;
    }

    if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, "Valid email is required");
        isValid = false;
    }

    if (!/^[6-9]\d{9}$/.test(phone.value.trim())) {
        showError(phone, "Phone must start with 6-9 and be 10 digits");
        isValid = false;
    }

    return isValid;
}
 
 
 
// Update Supplier
 
function openUpdateForm(id, supplier_name, company_name, supplier_email, address, supplier_phone,branch) {
    document.getElementById("supplierID").value = id;
    document.getElementById("supplier_name_change").value = supplier_name;
    document.getElementById("company_name_change").value = company_name;
    document.getElementById("supplier_email_change").value = supplier_email;
    document.getElementById("address_change").value = address;
    document.getElementById("supplier_phone_change").value = supplier_phone;
    document.getElementById("update_branch").value = branch;
  
    document.getElementById("updateOverlay").style.display = "block";
    document.getElementById("updateForm").style.display = "block";
  }
  
  function closeUpdateForm() {
    document.getElementById("updateOverlay").style.display = "none";
    document.getElementById("updateForm").style.display = "none";
  }
  function sureform(id){
    console.log("Setting bID to:", id);
    document.getElementById("SupID").value = id;
  
    document.getElementById("deleteOverlay").style.display = "block";
    document.getElementById("deleteForm").style.display = "block";
  }
  
  function  closedeleteForm(){
    document.getElementById("deleteOverlay").style.display = "none";
    document.getElementById("deleteForm").style.display = "none";
  }
  