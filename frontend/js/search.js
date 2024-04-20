function submitSearch() {
    var query = document.getElementById('searchInput').value;
    fetch('http://54.202.129.180:8000/retrieve-products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: query })
    })
        .then(response => response.json())
        .then(data => {
            const productsContainer = document.getElementById('productsContainer');
            productsContainer.innerHTML = ''; // Clear previous results

            data.products.forEach(product => {
                const productHTML = `
                    <div class="col-md-6 col-lg-4 col-xl-3">
                        <div class="rounded position-relative fruit-item">
                            <div class="fruit-img">
                                <img src="${product[12]}" class="img-fluid w-100 rounded-top" alt="">
                            </div>
                            <div class="p-4 border border-secondary border-top-0 rounded-bottom">
                                <h4>${product[0]}</h4>
                                <p>RAM:${product[5]}GB 
                                   ${product[6]}GB
                                   ${product[9]}""
                                   </p>
                                <div class="d-flex justify-content-between flex-lg-wrap">
                                    <p class="text-dark fs-5 fw-bold mb-0">$${product[11]}</p>
                                    <a href="#" class="btn border border-secondary rounded-pill px-3 text-primary"><i class="fa fa-shopping-bag me-2 text-primary"></i> Add to cart</a>
                                </div>
                            </div>
                        </div>
                    </div>`;
                productsContainer.innerHTML += productHTML;
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}