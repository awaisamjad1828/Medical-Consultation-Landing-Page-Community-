function calculateCGPA() {
    // Get the GPA values from the input fields
    let gpa1 = parseFloat(document.getElementById("gpa1").value);
    let gpa2 = parseFloat(document.getElementById("gpa2").value);
    let gpa3 = parseFloat(document.getElementById("gpa3").value);
    let gpa4 = parseFloat(document.getElementById("gpa4").value);
    let gpa5 = parseFloat(document.getElementById("gpa5").value);

    // Store the GPA values in an array
    let gpas = [gpa1, gpa2, gpa3, gpa4, gpa5];
    
    // Initialize variables for calculating CGPA
    let totalGpa = 0;
    let validGpasCount = 0;

    // Check validity for each GPA input
    for (let i = 0; i < gpas.length; i++) {
        if (gpas[i] >= 0.1 && gpas[i] <= 4.0) {
            totalGpa += gpas[i];
            validGpasCount++;
        } else if (gpas[i] !== '') {
            alert("Please enter a valid GPA between 0.1 and 4.0 for Semester " + (i + 1));
            return;
        }
    }

    // Check if at least one GPA is valid
    if (validGpasCount > 0) {
        // Calculate the CGPA by dividing the total GPA by the number of valid semesters
        let cgpa = totalGpa / validGpasCount;
        document.getElementById("result").innerText = cgpa.toFixed(2); // Display the CGPA
    } else {
        alert("Please enter valid GPA values for at least one semester.");
    }
}
