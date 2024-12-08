document.addEventListener('DOMContentLoaded', function() {
 
    fetch('/get_domains')
        .then(response => response.json())
        .then(data => {
            let domainList = document.querySelector('#domain-list ul');
            data.domains.forEach(domain => {
                let li = document.createElement('li');
                li.textContent = domain;
                domainList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching domains:', error));
});
