const API_BASE = "http://127.0.0.1:5000";

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
        .then(res => res.json())
        .then(data => {
            if (data.role === "teacher") {
                localStorage.setItem("user", JSON.stringify(data));
                window.location.href = "teacher.html";
            } else if (data.role === "student") {
                localStorage.setItem("user", JSON.stringify(data));
                window.location.href = `student${data.grade}.html`;
            } else {
                alert("⚠️ تأكد من صحة البيانات");
            }
        })
        .catch(err => {
            console.error(err);
            alert("حدث خطأ أثناء تسجيل الدخول");
        });
}
