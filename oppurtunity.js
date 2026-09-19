/* =========================================================
   SKILLBRIDGE STUDENT OPPORTUNITY PORTAL
========================================================= */


/* =========================================================
   API CONFIGURATION
========================================================= */

const API_URL =
    "http://127.0.0.1:8000/api/recommend";


/* =========================================================
   DOM ELEMENTS
========================================================= */

const recommendBtn =
    document.getElementById("recommendBtn");

const recommendations =
    document.getElementById("recommendations");

const loadingSection =
    document.getElementById("loadingSection");

const resultCount =
    document.getElementById("resultCount");

const profileSummary =
    document.getElementById("profileSummary");

const currentSkillCount =
    document.getElementById("currentSkillCount");

const opportunityCount =
    document.getElementById("opportunityCount");

const topMatch =
    document.getElementById("topMatch");

const menuButton =
    document.getElementById("menuButton");

const sidebar =
    document.getElementById("sidebar");

const editProfileBtn =
    document.getElementById("editProfileBtn");

const profileEdit =
    document.getElementById("profileEdit");


/* =========================================================
   GET STUDENT PROFILE
========================================================= */

function getStudentProfile() {

    const saved =
        localStorage.getItem(
            "skillbridge_student_profile"
        );


    if (!saved) {

        return {

            skills: [],

            certificates: [],

            projects: [],

            achievements: [],

            interests: [],

            education: "",

            experience: ""

        };
    }


    try {

        return JSON.parse(saved);

    } catch (error) {

        console.error(
            "Invalid profile data:",
            error
        );

        return {

            skills: [],

            certificates: [],

            projects: [],

            achievements: [],

            interests: [],

            education: "",

            experience: ""

        };
    }
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    if (value === null ||
        value === undefined) {

        return "";
    }


    return String(value)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");
}


/* =========================================================
   SAFE URL
========================================================= */

function safeURL(url) {

    if (!url) {
        return "#";
    }


    try {

        const parsed =
            new URL(
                url,
                window.location.origin
            );


        if (
            parsed.protocol === "http:" ||
            parsed.protocol === "https:"
        ) {

            return parsed.href;
        }


    } catch (error) {

        console.warn(
            "Invalid URL:",
            url
        );
    }


    return "#";
}


/* =========================================================
   DISPLAY PROFILE
========================================================= */

function displayProfile() {

    const profile =
        getStudentProfile();


    profileSummary.innerHTML = `

        <div class="profile-item">

            <label>
                Education
            </label>

            <strong>
                ${escapeHTML(
                    profile.education || "Not provided"
                )}
            </strong>

        </div>


        <div class="profile-item">

            <label>
                Skills
            </label>

            <strong>
                ${
                    profile.skills.length
                    ? escapeHTML(
                        profile.skills.join(", ")
                    )
                    : "No skills added"
                }
            </strong>

        </div>


        <div class="profile-item">

            <label>
                Interests
            </label>

            <strong>
                ${
                    profile.interests.length
                    ? escapeHTML(
                        profile.interests.join(", ")
                    )
                    : "No interests added"
                }
            </strong>

        </div>


        <div class="profile-item">

            <label>
                Projects
            </label>

            <strong>
                ${
                    profile.projects.length
                    ? escapeHTML(
                        profile.projects.join(", ")
                    )
                    : "No projects added"
                }
            </strong>

        </div>


        <div class="profile-item">

            <label>
                Certifications
            </label>

            <strong>
                ${
                    profile.certificates.length
                    ? escapeHTML(
                        profile.certificates.join(", ")
                    )
                    : "No certifications"
                }
            </strong>

        </div>


        <div class="profile-item">

            <label>
                Experience
            </label>

            <strong>
                ${
                    escapeHTML(
                        profile.experience ||
                        "No experience added"
                    )
                }
            </strong>

        </div>

    `;


    currentSkillCount.textContent =
        profile.skills.length;
}


/* =========================================================
   CREATE SKILL TAGS
========================================================= */

function createSkillTags(
    skills,
    missing = false
) {

    if (!skills || !skills.length) {

        return `
            <span class="skill-tag">
                None
            </span>
        `;
    }


    return skills.map(
        skill => `

            <span
                class="
                    skill-tag
                    ${missing ? "missing-tag" : ""}
                "
            >
                ${escapeHTML(skill)}
            </span>

        `
    ).join("");
}


/* =========================================================
   RENDER RECOMMENDATIONS
========================================================= */

function renderRecommendations(
    items
) {

    recommendations.innerHTML = "";


    if (!items || !items.length) {

        recommendations.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    ◇
                </div>

                <h3>
                    No matching opportunities found
                </h3>

                <p>
                    Try adding more skills,
                    interests or projects to your profile.
                </p>

            </div>

        `;

        resultCount.textContent =
            "0 opportunities";

        opportunityCount.textContent =
            "0";

        topMatch.textContent =
            "--";

        return;
    }


    resultCount.textContent =
        `${items.length} opportunities`;

    opportunityCount.textContent =
        items.length;


    const highestScore =
        Math.max(
            ...items.map(
                item =>
                    Number(item.match_score) || 0
            )
        );


    topMatch.textContent =
        `${Math.round(highestScore)}%`;


    items.forEach(item => {

        const score =
            Number(item.match_score) || 0;


        const matchedSkills =
            item.matched_skills || [];


        const missingSkills =
            item.missing_skills || [];


        const link =
            safeURL(item.link);


        const card =
            document.createElement("article");


        card.className =
            "recommendation-card";


        card.innerHTML = `

            <div class="recommendation-top">

                <div>

                    <span class="opportunity-type">

                        ${escapeHTML(
                            item.type ||
                            "Opportunity"
                        )}

                    </span>

                </div>


                <div class="match-score">

                    ${Math.round(score)}%

                </div>

            </div>


            <h3>

                ${escapeHTML(
                    item.title ||
                    "Untitled Opportunity"
                )}

            </h3>


            <div class="company">

                ${escapeHTML(
                    item.company ||
                    "Unknown Company"
                )}

            </div>


            <div class="location">

                📍 ${escapeHTML(
                    item.location ||
                    "Location not specified"
                )}

            </div>


            <p class="description">

                ${escapeHTML(
                    item.description ||
                    "No description available."
                )}

            </p>


            <div class="skill-label">

                MATCHED SKILLS

            </div>


            <div class="skill-tags">

                ${createSkillTags(
                    matchedSkills
                )}

            </div>


            ${
                missingSkills.length
                ? `

                    <div class="skill-label">

                        SKILLS TO IMPROVE

                    </div>


                    <div class="skill-tags">

                        ${createSkillTags(
                            missingSkills,
                            true
                        )}

                    </div>

                `
                : ""
            }


            <div class="skill-label">

                ELIGIBILITY

            </div>


            <p
                style="
                    font-size:12px;
                    color:#71818c;
                "
            >

                ${escapeHTML(
                    item.eligibility ||
                    "Check opportunity details."
                )}

            </p>


            <a
                class="apply-button"
                href="${link}"
                target="_blank"
                rel="noopener noreferrer"
            >

                View Opportunity →

            </a>

        `;


        recommendations.appendChild(
            card
        );

    });
}


/* =========================================================
   GET AI RECOMMENDATIONS
========================================================= */

async function getRecommendations() {

    const profile =
        getStudentProfile();


    /* Check profile */

    if (
        !profile.skills.length &&
        !profile.interests.length &&
        !profile.projects.length
    ) {

        alert(
            "Please complete your student profile first."
        );

        window.location.href =
            "basic-info.html";

        return;
    }


    /* Show loading */

    loadingSection.classList.remove(
        "hidden"
    );


    recommendations.innerHTML = "";


    try {

        const response =
            await fetch(
                API_URL,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(profile)

                }
            );


        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );
        }


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                "Recommendation request failed."
            );
        }


        renderRecommendations(
            data.recommendations || []
        );


    } catch (error) {

        console.error(
            "Recommendation error:",
            error
        );


        recommendations.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    ⚠
                </div>

                <h3>
                    Unable to connect to SkillBridge AI
                </h3>

                <p>
                    Make sure the FastAPI backend is
                    running on port 8000.
                </p>

                <p style="
                    margin-top:10px;
                    font-size:11px;
                ">

                    ${escapeHTML(
                        error.message
                    )}

                </p>

            </div>

        `;


    } finally {

        loadingSection.classList.add(
            "hidden"
        );

    }
}


/* =========================================================
   MOBILE MENU
========================================================= */

if (menuButton) {

    menuButton.addEventListener(
        "click",
        () => {

            sidebar.classList.toggle(
                "open"
            );

        }
    );
}


/* =========================================================
   EDIT PROFILE
========================================================= */

function editProfile() {

    window.location.href =
        "basic-info.html";
}


if (editProfileBtn) {

    editProfileBtn.addEventListener(
        "click",
        editProfile
    );
}


if (profileEdit) {

    profileEdit.addEventListener(
        "click",
        editProfile
    );
}


/* =========================================================
   RECOMMEND BUTTON
========================================================= */

if (recommendBtn) {

    recommendBtn.addEventListener(
        "click",
        getRecommendations
    );
}


/* =========================================================
   NAVIGATION ACTIVE STATE
========================================================= */

const navLinks =
    document.querySelectorAll(
        ".nav-link"
    );


navLinks.forEach(link => {

    link.addEventListener(
        "click",
        () => {

            navLinks.forEach(
                item =>
                    item.classList.remove(
                        "active"
                    )
            );


            link.classList.add(
                "active"
            );


            if (
                window.innerWidth <= 750
            ) {

                sidebar.classList.remove(
                    "open"
                );
            }

        }
    );

});


/* =========================================================
   INITIALIZE
========================================================= */

displayProfile();