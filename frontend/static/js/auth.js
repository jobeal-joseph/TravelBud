const signupForm = document.getElementById("signupForm");
const loginForm = document.getElementById("loginForm");

if (signupForm) {
 signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Updated URL to match your Flask Blueprint route
    const res = await fetch("/auth/signup", { 
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      })
    });

    const data = await res.json();
    if (res.ok) {
      alert("Signup successful! Redirecting to login...");
      console.log("Signup success, attempting redirect...");
      window.location.replace("/auth/login");
    } else {
      alert(data.error || "Signup failed");
    }
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Updated URL to match your Flask Blueprint route
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
      })
    });

    if (res.ok) {
      window.location.href = "/dashboard"; // Go to dashboard on success
    } else {
      const data = await res.json();
      alert(data.error || "Invalid credentials");
    }
  });
}
