document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.minus').forEach(button => {
        button.addEventListener('click', function() {
            var room = button.dataset.room;
            var count = document.getElementById(room + '-count').innerText;
            if (count > 1) {
                document.getElementById(room + '-count').innerText = parseInt(count) - 1;
            }
        });
    });

    document.querySelectorAll('.plus').forEach(button => {
        button.addEventListener('click', function() {
            var room = button.dataset.room;
            var count = document.getElementById(room + '-count').innerText;
            document.getElementById(room + '-count').innerText = parseInt(count) + 1;
        });
    });

    document.getElementById('next-btn-1').addEventListener('click', function() {
        var bhkSelected = document.querySelector('input[name="bhk"]:checked');
        if (bhkSelected) {
            document.getElementById('bhk-step').classList.remove('active');
            document.getElementById('rooms-step').classList.add('active');
            document.getElementById('bhk-nav').classList.remove('active');
            document.getElementById('rooms-nav').classList.add('active');
            document.getElementById('progress-text').innerText = '2/4';
        } else {
            alert('Please select a BHK type');
        }
    });

    document.getElementById('back-btn-1').addEventListener('click', function() {
        document.getElementById('rooms-step').classList.remove('active');
        document.getElementById('bhk-step').classList.add('active');
        document.getElementById('rooms-nav').classList.remove('active');
        document.getElementById('bhk-nav').classList.add('active');
        document.getElementById('progress-text').innerText = '1/4';
    });

    document.getElementById('next-btn-2').addEventListener('click', function() {
        document.getElementById('rooms-step').classList.remove('active');
        document.getElementById('package-step').classList.add('active');
        document.getElementById('rooms-nav').classList.remove('active');
        document.getElementById('package-nav').classList.add('active');
        document.getElementById('progress-text').innerText = '3/4';
    });

    document.getElementById('back-btn-2').addEventListener('click', function() {
        document.getElementById('package-step').classList.remove('active');
        document.getElementById('rooms-step').classList.add('active');
        document.getElementById('package-nav').classList.remove('active');
        document.getElementById('rooms-nav').classList.add('active');
        document.getElementById('progress-text').innerText = '2/4';
    });

    document.getElementById('next-btn-3').addEventListener('click', function() {
        var packageSelected = document.querySelector('input[name="package"]:checked');
        if (packageSelected) {
            document.getElementById('package-step').classList.remove('active');
            document.getElementById('quote-step').classList.add('active');
            document.getElementById('package-nav').classList.remove('active');
            document.getElementById('quote-nav').classList.add('active');
            document.getElementById('progress-text').innerText = '4/4';
        } else {
            alert('Please select a package');
        }
    });

    document.getElementById('back-btn-3').addEventListener('click', function() {
        document.getElementById('quote-step').classList.remove('active');
        document.getElementById('package-step').classList.add('active');
        document.getElementById('quote-nav').classList.remove('active');
        document.getElementById('package-nav').classList.add('active');
        document.getElementById('progress-text').innerText = '3/4';
    });

    document.getElementById('submit-btn').addEventListener('click', function(event) {
        event.preventDefault();
        var name = document.getElementById('name').value;
        var email = document.getElementById('email').value;
        var phone = document.getElementById('phone').value;
        var property = document.getElementById('property').value;

        if (name && email && phone && property) {
            alert('Quote submitted successfully!');
            // Add logic here to handle form submission
        } else {
            alert('Please enter your name, email ID, phone number, and property name');
        }
    });
});
