document.addEventListener("DOMContentLoaded", function() {
    loadPets('All', 'All');
});

let currentType = 'All';

function loadPets(type, city) {
    currentType = type;
    let url = `/api/pets?type=${type}&city=${city}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("pets-list");
            if (data.length === 0) {
                container.innerHTML = `<div class="col-12"><p class="text-muted">Nema pronađenih ljubimaca za izabrane filtere.</p></div>`;
                return;
            }
            container.innerHTML = data.map(pet => `
                <div class="col-md-4 mb-4">
                    <div class="card h-100 shadow-sm border-0 rounded overflow-hidden">
                        <img src="${pet.image}" class="card-img-top" style="height: 220px; object-fit: cover;" alt="${pet.name}">
                        <div class="card-body d-flex flex-column">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h4 class="card-title m-0 fw-bold">${pet.name}</h4>
                                <span class="badge bg-success">${pet.type}</span>
                            </div>
                            <h6 class="text-muted mb-2">📍 ${pet.city} | 🎂 ${pet.age}</h6>
                            <p class="text-secondary small mb-2"><strong>Rasa:</strong> ${pet.breed}</p>
                            <p class="card-text text-dark flex-grow-1">${pet.description}</p>
                            <div class="bg-light p-2 rounded mb-3 border">
                                <small class="text-muted d-block">Kontakt: <strong>${pet.owner}</strong></small>
                                <small class="text-success fw-bold">📞 ${pet.phone}</small>
                            </div>
                            <button class="btn btn-outline-success w-100 fw-bold" onclick="contactOwner('${pet.owner}', '${pet.phone}')">Kontaktiraj vlasnika</button>
                        </div>
                    </div>
                </div>
            `).join('');
        });
}

function filterPets(type, cityArg) {
    const city = document.getElementById("city-filter").value;
    loadPets(type, city);
}

function applyFilters() {
    const city = document.getElementById("city-filter").value;
    loadPets(currentType, city);
}

function addNewPet(event) {
    event.preventDefault();
    
    const name = document.getElementById("pet-name").value;
    const type = document.getElementById("pet-type").value;
    const breed = document.getElementById("pet-breed").value;
    const city = document.getElementById("pet-city").value;
    const age = document.getElementById("pet-age").value;
    const owner = document.getElementById("pet-owner").value;
    const phone = document.getElementById("pet-phone").value;
    const description = document.getElementById("pet-desc").value;

    fetch('/api/pets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, type, breed, city, age, owner, phone, description })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("add-pet-form").reset();
            loadPets('All', 'All');
            alert("Oglas je uspešno postavljen!");
        }
    });
}

function contactOwner(owner, phone) {
    alert(`Kontakt podaci vlasnika/azila:\n\nNaziv: ${owner}\nTelefon: ${phone}\n\nMožete ih pozvati radi dogovora o udomljavanju!`);
}