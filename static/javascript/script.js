// Dis plays the div or page associated with the clicked tablink
function openPage(pageName, elmnt) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        var currentTabLink = tablinks[i];
        currentTabLink.style.borderBottom = "";
        currentTabLink.style.backgroundColor = "";
        currentTabLink.setAttribute("id", "");
    }

    // Show the specific tab content
    document.getElementById(pageName).style.display = "block";

    // Highlight button used to open tab
    elmnt.style.borderBottom = "thick solid #FF7900";
    elmnt.setAttribute("id", "defaultOpen");
    //elmnt.style.backgroundColor = "#f2c196";
}

// Show/Hide an element 
function toggleShowHide(elmnt) {
  if (document.getElementById(elmnt).style.display === "") {
    document.getElementById(elmnt).style.display = "block";
  } else {
    document.getElementById(elmnt).style.display = "";
  }
}

function toggleShowHideChildren(elmnt) {
  let menu = elmnt.children[1];

  if (menu.style.display === "") {
    menu.style.display = "block";
  } else {
    menu.style.display = "";
  }
}

// Sends data request and retrieves simulated result
async function runSimulation(elmnt) {
  // Obtains csrf_token from document for security reasons
  const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

  const pipe_label = elmnt.name;

  const response = await fetch("/simulation.result/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf_token,
    },
    body: JSON.stringify({
      pipe_label: pipe_label,
      csrfmiddlewaretoken: csrf_token,
    }),
  });

  // Check response status code
  if (response.status === 200) {
    // The response was successful
    const json_data = await response.json();

    for (const leak in json_data) {
      newLeak = json_data[`${leak}`];

      var leak_location = newLeak["leak_location"];

      var results_container = document.getElementById("result");
      results_container.innerHTML = "";

      // New div element for current leak
      var leak_display_container = document.createElement("div");

      // Velocity Label
      var v_label = document.createElement("label");
      v_label.textContent = "Velocity Distribution";
      v_label.setAttribute("class", "leak-display-label");
      console.log(v_label)

      // Pressure Label
      var p_label = document.createElement("label");
      p_label.innerHTML = "Pressure Distribution";
      p_label.setAttribute("class", "leak-display-label");

      // Inserts template of leak details into the new element
      leak_display_container.innerHTML = document.getElementById("result-template").innerHTML;
      
      // Populates the new element with leak details using the inserted template
      var leak_details = leak_display_container.children;
      leak_details[0].innerHTML = `Leak Detected Between ${leak_location[0]} and ${leak_location[1]} Section!!!`;
      leak_details[0].classList.add("blink");

      leak_details[1].innerHTML = `Leak size: ${newLeak.leak_size} ${mass_rate[newLeak.unit]}`;
      leak_details[1].classList.add("blink");

      var v_plot = leak_details[2].children[0];
      v_plot.classList.add("fade");
      v_plot.setAttribute("src", `/static/images/${newLeak.v_plot}`);
      leak_details[2].appendChild(v_label);

      var p_plot = leak_details[3].children[0];
      p_plot.classList.add("fade");
      p_plot.setAttribute("src", `/static/images/${newLeak.p_plot}`);
      leak_details[3].appendChild(p_label);

      // Appends the now populated container into the results container
      results_container.appendChild(leak_display_container);
    }
  } else {
    // The request failed
    console.log("The request failed!");
  }
}

// Handles Units
mass_rate = {
  "Field Units": "lb/s",
  "S.I Units": "Kg/s",
}

// Homepage slides
var slides = [
  "LN_base_local_IMG_0052_Original.jpg", 
  "LN_base_local_IMG_0045_Original.jpg", 
  "LN_base_local_IMG-20230827-WA0002.jpg",
]
let x = 1;

let noOfSlides = slides.length;

setInterval(function() {
  var nextSlide = x % (noOfSlides + 1);
  var slide_image = document.getElementById("slide-img");
  slide_image.src = `/static/images/${slides[nextSlide]}`;

  // Removes the fade class from the image, trigger a reflow and re-add the fade class to the slide image
  slide_image.classList.remove("fade");
  void slide_image.offsetWidth;
  slide_image.classList.add("fade");
  
  x++;

  if (x === noOfSlides) {
    x = 0;
  }
}, 5000);

// Gets the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

// Gets all created pipe data
var pipeDataElmts = document.getElementsByClassName("available-pipe-data");
for (var i = 0; i < pipeDataElmts.length; i++) {
  // Gets children of current pipe data element
  var pipeDataSubElmts = pipeDataElmts[i].children;
  var pipe_label = pipeDataSubElmts[0].innerHTML;
  pipeDataSubElmts[1].children[0].setAttribute("name", pipe_label);
}
