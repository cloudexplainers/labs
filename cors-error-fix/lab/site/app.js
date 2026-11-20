// Driftwood Surf School booking page. The lessons live on the API, a different site from this page.
const API = "http://api.surf.test";
const list = document.getElementById("lessons");
const status = document.getElementById("status");

function show(text, ok) {
  status.textContent = text;
  status.className = "status " + (ok ? "ok" : "bad");
}

async function loadLessons() {
  try {
    const res = await fetch(API + "/lessons");
    const lessons = await res.json();
    list.innerHTML = "";
    for (const l of lessons) {
      const li = document.createElement("li");
      li.id = "lesson-" + l.id;
      li.innerHTML = `<span class="when">${l.when}</span><span class="what">${l.what}</span>` +
        `<span class="spaces">${l.spaces ? l.spaces + (l.spaces === 1 ? " space left" : " spaces left") : "full"}</span><button>Book</button>`;
      li.querySelector("button").onclick = () => book(l.id);
      list.appendChild(li);
    }
  } catch (err) {
    list.innerHTML = `<li class="error">Couldn't load lessons (${err})</li>`;
  }
}

async function book(id) {
  try {
    const res = await fetch(API + "/bookings", {
      method: "POST",
      credentials: "include",                       // send the customer's sign-in cookie
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lesson: id, name: "Maya" }),
    });
    const body = await res.json();
    if (res.ok) show("Booked: " + body.booked, true);
    else show("Sorry: " + body.error + " (" + res.status + ")", false);
  } catch (err) {
    show("Booking failed (" + err + ")", false);
  }
}

loadLessons();
