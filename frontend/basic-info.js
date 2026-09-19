const profileForm =
    document.getElementById("profileForm");


function splitValues(value) {

    if (!value) {
        return [];
    }

    return value
        .split(/[,;\n]+/)
        .map(item => item.trim())
        .filter(Boolean);
}


profileForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();


        const profile = {

            education:
                document
                    .getElementById("education")
                    .value
                    .trim(),

            skills:
                splitValues(
                    document
                        .getElementById("skillsInput")
                        .value
                ),

            certificates:
                splitValues(
                    document
                        .getElementById("certificates")
                        .value
                ),

            projects:
                splitValues(
                    document
                        .getElementById("projects")
                        .value
                ),

            achievements:
                splitValues(
                    document
                        .getElementById("achievements")
                        .value
                ),

            interests:
                splitValues(
                    document
                        .getElementById("interests")
                        .value
                ),

            experience:
                document
                    .getElementById("experience")
                    .value
                    .trim()

        };


        /* Save profile */

        localStorage.setItem(
            "skillbridge_student_profile",
            JSON.stringify(profile)
        );


        /* Go to opportunity page */

        window.location.href =
            "oppurtunity.html";

    }
);