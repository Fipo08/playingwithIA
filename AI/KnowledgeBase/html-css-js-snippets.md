# HTML / CSS / JS Snippets

## Fetch API
```javascript
// GET
const res = await fetch("/api/data");
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const data = await res.json();

// POST
const res = await fetch("/api/data", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({name: "test"}),
});
```

## Promesas y async/await
```javascript
const delay = ms => new Promise(r => setTimeout(r, ms));

async function main() {
  try {
    const [a, b] = await Promise.all([fetchA(), fetchB()]);
    console.log(a, b);
  } catch (err) {
    console.error(err);
  }
}
```

## CSS Grid
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}
```

## CSS Flexbox
```css
.flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

## Formularios (JS)
```javascript
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  // enviar data
});
```

## Template strings
```javascript
const html = `
  <div class="card">
    <h2>${title}</h2>
    <p>${description}</p>
  </div>
`;
```
