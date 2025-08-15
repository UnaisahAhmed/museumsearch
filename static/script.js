<script>
    document.addEventListener("DOMContentLoaded", function() {
        const popularItems = [
            { id: 1, title: "The Metropolitan Museum of Art", image: "https://upload.wikimedia.org/wikipedia/commons/0/0b/The_Metropolitan_Museum_of_Art%2C_New_York.jpg" },
            { id: 2, title: "The Museum of Modern Art", image: "https://upload.wikimedia.org/wikipedia/commons/c/c0/Museum_of_Modern_Art_entrance_2008.jpg" },
            { id: 3, title: "The American Museum of Natural History", image: "https://upload.wikimedia.org/wikipedia/commons/d/d4/American_Museum_of_Natural_History_exterior.jpg" },
        ];

        const popularItemsContainer = document.querySelector(".row");
        popularItems.forEach(item => {
            const card = document.createElement("div");
            card.classList.add("col-md-4");
            card.innerHTML = `
                <div class="card">
                    <img src="${item.image}" class="card-img-top" alt="Museum Image">
                    <div class="card-body">
                        <h5 class="card-title">${item.title}</h5>
                        <a href="/view/${item.id}" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            `;
            popularItemsContainer.appendChild(card);
        });
    });

// Function to handle the search
    function handleSearch() {
        const searchQuery = document.getElementById("searchInput").value; // Get the value from the input field

        // if the search query consists only of whitespace
        if (!searchQuery.trim()) {
            // Clear the text box without changing the state
            document.getElementById("searchInput").value = ''; 
            return; // Don't perform any search logic
        }

        // go with with your existing search logic here

        performSearch(searchQuery);
    }

    // Function to perform the actual search
    function performSearch(query) {
        // Your search logic here, e.g., filter through museums
        console.log("Searching for:", query);
    }

    


</script>
