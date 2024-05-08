# The Dream Is Now

# Taka API README
=====================

Welcome to the Taka API, a platform that generates stories based on photos/pictures.

## Overview
------------

The Taka API is built using Django and Django Rest Framework, and provides the following features:

* Upload photos and generate stories (text and audio)
* Retrieve or search popular photos from [pexels.com](https://www.pexels.com/)
* Documentation with Swagger and Redoc

## Endpoints
------------

### Media Endpoints

* **GET /media/photos/<str:topic>**: Retrieve photos by topic
* **GET /media/populars/**: Retrieve popular photos (paginated)
* **GET /media/populars/<int:page_number>**: Retrieve next page of popular photos

### Stories Endpoints

* **POST /stories/<str:type>**: Retrieve story from image (image or url) (type: e.g. "image")

### Documentation Endpoints

* **GET /docs/swagger<format>**: Get Swagger JSON documentation
* **GET /docs/swagger/**: Get Swagger UI documentation
* **GET /docs/redoc/**: Get Redoc documentation

## Setup
--------

1. Clone the repository and navigate to the project directory
2. Install dependencies with `pip install -r requirements.txt`
3. Run the server with `python manage.py runserver`
4. Access the API at `http://localhost:8000`

## Contact
----------

For any issues or questions, please contact [ikeecode@gmail.com](mailto:ikeecode@gmail.com)

## License
----------

This project is licensed under the MEST@africa License. See [LICENSE](LICENSE) for details.