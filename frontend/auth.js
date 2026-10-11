function getLoggedInUser() {
    const user = localStorage.getItem("careerPathUser");

    if (!user) {
        return null;
    }

    try {
        return JSON.parse(user);
    } catch (error) {
        localStorage.removeItem("careerPathUser");
        return null;
    }
}


function requireLogin() {
    const user = getLoggedInUser();

    if (!user) {
        window.location.href = "/static/login.html";
        return null;
    }

    return user;
}


function logoutUser() {
    localStorage.removeItem("careerPathUser");
    localStorage.removeItem("careerPathProfile");
    localStorage.removeItem("resumeAnalysis");

    window.location.href = "/static/login.html";
}