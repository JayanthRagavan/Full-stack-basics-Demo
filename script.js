document.getElementById('infoForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const name = document.getElementById('nameInput').value;

  const response = await fetch('/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });

  const data = await response.json();

  document.getElementById('responseMessage').textContent = data.message;

  // Show updated user list
  const userList = document.getElementById('userList');
  userList.innerHTML = ''; // Clear previous list

  data.users.forEach(user => {
    const li = document.createElement('li');
    li.textContent = `${user.id}. ${user.name}`;
    userList.appendChild(li);
  });
});
