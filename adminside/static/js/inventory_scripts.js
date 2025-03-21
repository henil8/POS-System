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
    let itemname = row.cells[2].textContent.trim().toLowerCase();
    let category = row.cells[3].textContent.trim().toLowerCase();

    if (itemname.includes(filter) || category.includes(filter)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});


let foodItemId = 1;

document.addEventListener("DOMContentLoaded", function () {
 document.getElementById("foodItemForm").addEventListener("submit", function (event) {
      
      
        document.getElementById("foodItemForm").submit();
      
    });
  document.getElementById("updateForm").addEventListener("submit", function (event) {
      
      
      document.getElementById("updateForm").submit();
    
  });


});


// function populateStaticDropdowns() {
//   let names = ["Pizza", "Burger", "Pasta"];


//   let nameDropdown = document.getElementById("itemName");


//   names.forEach(name => {
//     let option = document.createElement("option");
//     option.value = name;
//     option.textContent = name;
//     nameDropdown.appendChild(option);
//   });


// }

function validateForm() {

  let itemCategory = document.getElementById("itemCategory");
  let item_name=document.getElementById("itemName");
  let itemQuantity=document.getElementById("itemQuantity");

  let itemCategoryValue = itemCategory.value.trim();
  let item_nameValue=item_name.value.trim();
  let itemQuantityValue=itemQuantity.value.trim();

  removeError(itemCategory);
  removeError(item_name);
  removeError(itemQuantity);
  clearErrors();

  let isValid = true;
  
  if (!item_nameValue) {
      showError(item_name, " Name is required");
      isValid = false;
  }
 

  if (!itemCategoryValue) {
    showError(itemCategory, "Category is required");
    isValid = false;
  }

  if (!itemQuantityValue) {
    showError(itemQuantity, "Quantity is required");
    isValid = false;
  }

  return isValid;
}

function openUpdateForm(id) {
  // document.getElementById("overlay").style.display = "block";
  // document.getElementById("myForm").style.display = "block";
  // document.body.classList.add("popup-open");

  fetch(`/adminside/get_update_form/${id}/`)  // Fetch the form from Django
      .then(response => response.text())  // Convert response to HTML
      .then(html => {
          document.getElementById("updateitemID").value = id;  // Set hidden input ID
          document.getElementById("updateFormFields").innerHTML = html;  // Inject form fields
          document.getElementById("updateOverlay").style.display = "block";  // Show overlay
          document.getElementById("updateForm").style.display = "block";  // Show popup
      })
      .catch(error => console.error("Error fetching form:", error));
      //document.getElementById("updateitemID").value = id;// Set hidden input ID
          // document.getElementById("updateitemImage").value = image;
          // document.getElementById("updateitemName").value = name;  
          // document.getElementById("updateitemCategory").value = category;  
          // document.getElementById("updateitemquantity").value = quantity;  
          // document.getElementById("updateitemdescription").value = Description;  
          // document.getElementById("updateitemCostprice").value = costprice;  
          // document.getElementById("updateitemSellprice").value = sellprice;  
          // document.getElementById("updateitemMfg_date").value = mfg_date;
          // document.getElementById("updateitemExp_date").value = exp_date;

}


function closeUpdateForm() {
  document.getElementById("updateOverlay").style.display = "none";
  document.getElementById("updateForm").style.display = "none";
}

function showUpdatePopup(button) {
  var id = button.getAttribute("data-id");  
  var form = document.getElementById("updateForm");  

  // Set the hidden input field with the item ID
  document.getElementById("updateitemID").value = id;

  // Show the popup
  form.style.display = "block";
}

// function addFoodItem() {
//   let itemName = document.getElementById("itemName");
//   let itemCategory = document.getElementById("itemCategory");
//   let itemDescription = document.getElementById("itemDescription");
//   let itemQuantity = document.getElementById("itemQuantity");
//   let itemStore = document.getElementById("itemStore");
//   let itemCost = document.getElementById("itemCost");
//   let itemSelling = document.getElementById("itemSelling");
//   let itemMFG = document.getElementById("itemMFG");
//   let itemExpiry = document.getElementById("itemExpiry");


//   clearErrors();

//   let isValid=true;

//   if (!itemName.value.trim()) {
//     showError("nameError", "Item name is required.");
//     isValid = false;
//   }
//   if (!itemCategory.value.trim()) {
//     showError("categoryError", "Category is required.");
//     isValid = false;
//   }
//   if (!itemDescription.value.trim()) {
//     showError("descriptionError", "Description is required.");
//     isValid = false;
//   }
//   if (!itemQuantity.value.trim() || isNaN(itemQuantity.value) || itemQuantity.value <= 0) {
//     showError("quantityError", "Enter a valid quantity.");
//     isValid = false;
//   }
//   if (!itemStore.value.trim()) {
//     showError("storeError", "Store selection is required.");
//     isValid = false;
//   }
//   if (!itemCost.value.trim() || isNaN(itemCost.value) || itemCost.value <= 0) {
//     showError("costPriceError", "Enter a valid cost.");
//     isValid = false;
//   }
//   if (!itemSelling.value.trim() || isNaN(itemSelling.value) || itemSelling.value <= 0) {
//     showError("sellingPriceError", "Enter a valid selling price.");
//     isValid = false;
//   }
//   if (!itemMFG.value.trim()) {
//     showError("MFG-Error", "Manufacturing date is required.");
//     isValid = false;
//   }
//   if (!itemExpiry.value.trim()) {
//     showError("expiryError", "Expiry date is required.");
//     isValid = false;
//   }

//   if (!isValid) return; 

//   let newRow = document.createElement("tr");
//   newRow.innerHTML = `
//         <td>${foodItemId}</td>
//         <td>Image</td>
//         <td>${itemName.value}</td>
//         <td>${itemCategory.value}</td>
//         <td>${itemDescription.value}</td>
//         <td>${itemQuantity.value}</td>
//         <td>${itemStore.value}</td>
//         <td>${itemCost.value}</td>
//         <td>${itemSelling.value}</td>
//         <td>${itemMFG.value}</td>
//         <td>${itemExpiry.value}</td>
//         <td>
//             <button class="update-btn" onclick="updateRow(this)"><i class="fas fa-edit"></i></button>
//             <button class="delete-btn" onclick="deleteRow(this)"><i class="fas fa-trash"></i></button>
//         </td>
//     `;

//   document.getElementById("foodTableBody").appendChild(newRow);
//   foodItemId++;

//   document.getElementById("foodItemForm").reset();
//   closeForm();
// }

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

function updateRow(button) {
  let row = button.closest("tr");
  let columns = row.getElementsByTagName("td");

  document.getElementById("itemName").value = columns[2].innerText;
  document.getElementById("itemCategory").value = columns[3].innerText;
  document.getElementById("itemDescription").value = columns[4].innerText;
  document.getElementById("itemQuantity").value = columns[5].innerText;
  document.getElementById("itemStore").value = columns[6].innerText;
  document.getElementById("itemCost").value = columns[7].innerText;
  document.getElementById("itemSelling").value = columns[8].innerText;
  document.getElementById("itemMFG").value = columns[9].innerText;
  document.getElementById("itemExpiry").value = columns[10].innerText;

  openForm();
  row.remove(); 
}

function deleteRow(button) {
  button.closest("tr").remove();
}

function openForm() {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");
}

function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");
}
