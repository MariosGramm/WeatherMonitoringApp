# WeatherMonitoringApp
A cloud-based weather monitoring API built with Flask, deployed on Azure App Service, and integrated with Prometheus for metrics, Grafana for dashboards and Telegram for real-time alerts.


Αυτό το project είναι ένα σύστημα παρακολούθησης και ειδοποιήσεων για δεδομένα καιρού, το οποίο αναπτύχθηκε με τη χρήση Flask, Prometheus, Alertmanager, Grafana και Docker.

 Flask API στο Azure App Service:
Η κύρια εφαρμογή είναι ένα Flask API, το οποίο τρέχει online στο Azure App Service και παραμένει διαθέσιμο για πάντα, καθώς δεν υπάρχει χρέωση για τη χρήση του. Το API παρέχει τις εξής λειτουργίες:

/weather: Endpoint που επιστρέφει δεδομένα καιρού, όπως θερμοκρασία, υγρασία, ταχύτητα ανέμου και καιρικές συνθήκες.

/metrics: Endpoint που εκθέτει τις μετρικές του API σε μορφή που μπορεί να διαβαστεί από το Prometheus. Περιλαμβάνει δεδομένα για τον χρόνο απόκρισης του API, τα συνολικά αιτήματα και τον αριθμό των ενεργών χρηστών.

/ (Route endpoint): Μια βασική διαδρομή που απλά επιβεβαιώνει ότι το API λειτουργεί σωστά.


 Prometheus για συλλογή μετρικών:
Το Prometheus είναι υπεύθυνο για τη συλλογή μετρικών από το API, όπως η θερμοκρασία, η υγρασία, η ταχύτητα του ανέμου, καθώς και δεδομένα σχετικά με την απόκριση και τη χρήση του API.

 Alertmanager για ειδοποιήσεις:
Σε περίπτωση που οι μετρικές ξεπεράσουν συγκεκριμένα όρια (π.χ. πολύ υψηλή θερμοκρασία, χαμηλή απόκριση API), το Alertmanager ενεργοποιεί ειδοποιήσεις που αποστέλλονται μέσω Telegram.

 Grafana για οπτικοποίηση δεδομένων:
Οι μετρικές αποθηκεύονται και εμφανίζονται σε dashboards στο Grafana, επιτρέποντας την εύκολη παρακολούθηση των τάσεων και της απόδοσης του API.

Υποδομή και Τεχνολογίες:

- Το Flask API τρέχει πάνω στο Azure App Service και είναι online.
- Prometheus, Alertmanager και Grafana τρέχουν τοπικά σε Docker Containers.
- Τα δεδομένα συλλέγονται real-time από το API και αποθηκεύονται στο Prometheus, ενώ οι ειδοποιήσεις αποστέλλονται μέσω του Alertmanager στο Telegram.

Το σύστημα αυτό είναι κατάλληλο για παρακολούθηση δεδομένων καιρού σε πραγματικό χρόνο, με δυνατότητα ειδοποιήσεων όταν εντοπίζονται κρίσιμες αλλαγές στις μετρήσεις.





This project is a weather monitoring and alerting system developed using Flask, Prometheus, Alertmanager, Grafana, and Docker.

Flask API on Azure App Service:

The core application is a Flask API, which runs online on Azure App Service and will remain available indefinitely, as there are no associated costs. The API provides the following functionalities:

/weather: An endpoint that returns weather data, including temperature, humidity, wind speed, and weather conditions.

/metrics: An endpoint that exposes API metrics in a format readable by Prometheus. It includes data such as API response time, total requests, and active users.

/ (Route endpoint): A basic route that simply confirms the API is running correctly.

Prometheus for Metrics Collection:

Prometheus is responsible for collecting metrics from the API, such as temperature, humidity, wind speed, and performance-related data like response time and API usage.

Alertmanager for Notifications:

If any metrics exceed predefined thresholds (e.g., extreme temperatures, high API response time), Alertmanager triggers alerts that are sent via Telegram.

Grafana for Data Visualization:

All collected metrics are stored and visualized in Grafana dashboards, making it easy to track trends and monitor API performance.

Infrastructure and Technologies Used:

-The Flask API runs on Azure App Service and is publicly accessible.
-Prometheus, Alertmanager, and Grafana run locally in Docker containers.
-Weather data is collected in real-time from the API, stored in Prometheus, and alerts are sent via Alertmanager to Telegram.

This system is ideal for real-time weather monitoring, with built-in alerting capabilities whenever critical changes in the collected metrics are detected.
