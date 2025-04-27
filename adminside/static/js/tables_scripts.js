document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("tableForm").addEventListener("submit", function (event) {

        document.getElementById("tableForm").submit();
    });

   

    document.getElementById("FormDelete").addEventListener("submit", function (event) {
        this.submit();
    });

    populateStaticDropdowns();
});

function populateStaticDropdowns() {
    let statuss = ["Active", "Disabled"];
    let statusDropdown = document.getElementById("status");
    if (statusDropdown.options.length === 1) {
        statuss.forEach((status) => {
            let option = document.createElement("option");
            option.value = status;
            option.textContent = status;
            statusDropdown.appendChild(option);
        });
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

function removeError(input) {
    let error = input.parentNode.querySelector(".error-message");
    if (error) {
        error.remove();
    }
}

function clearErrors() {
    document.querySelectorAll(".error-message").forEach((el) => {
        el.textContent = "";
    });
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

  
  function openUpdateForm(id, table_id, seats, status) {
    document.getElementById("tabId").value = id; // this must be table.id
    document.getElementById("updateTable_id").value = table_id;
    document.getElementById("updateseats").value = seats;
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
    document.getElementById("tID").value = id;
  
    document.getElementById("deleteOverlay").style.display = "block";
    document.getElementById("deleteForm").style.display = "block";
  }
  
  function  closedeleteForm(){
    document.getElementById("deleteOverlay").style.display = "none";
    document.getElementById("deleteForm").style.display = "none";
  }