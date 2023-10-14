import os
from flask import Flask, request, abort, jsonify
from models import setup_db
from flask_cors import CORS
from models import Actor, Movie, db_drop_and_create_all
from auth import requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/actors', methods=["GET"])
    @requires_auth('read:actors')
    def get_actors():
        if request.method == "GET":
            actors = Actor.query.all()
            if len(actors) == 0:
                abort(404)

            return jsonify({
                'actors': actors,
                'success': True
            })
    
    @app.route('/actors/<int:id>', methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(id):
        selected_actor = Actor.query.filter_by(id=id).first()

        if selected_actor is None:
            abort(404)
        try:
            selected_actor.delete()
            return jsonify({
                'success': True,
                'actor': id
            })
        except:
            abort(405)

    @app.route('/actors', methods=["POST"])
    @requires_auth('create:actors')
    def add_actor():
        try:
            body = request.get_json()
            new_actor_name = body.get('name')
            new_actor_age = body.get('age')
            new_actor_gender = body.get('gender')
            new_actor_detail = Actor(
                name=new_actor_name,
                age=new_actor_age,
                gender=new_actor_gender
            )

            new_actor_detail.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)
            
    @app.route('/actors/<int:id>', methods=["PATCH"])
    @requires_auth('update:actors')
    def update_actor(id):
        body = request.get_json()
        if not body:
            abort(422)
        
        try:
            actor = Actor.query.get(id)
        except:
            abort(404)
            
        actor.update()
        return jsonify({
            'success': True,
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        })
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movies')
    def get_movies():
        movie = Movie.query.all()
        if len(movie) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "movies": movie
        })
        
    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(id):
        selected_movie = Movie.query.filter_by(id=id).first()

        if selected_movie is None:
            abort(404)
        try:
            selected_movie.delete()
            return jsonify({
                'success': True,
                'movie': id
            })
        except:
            abort(405)

    @app.route('/movies', methods=["POST"])
    @requires_auth('create:movies')
    def add_movie():
        try:
            body = request.get_json()
            new_movie_name = body.get('title')
            new_movie_release_date = body.get('release_date')
            new_movie_detail = Movie(
                title=new_movie_name,
                release_date=new_movie_release_date
            )

            new_movie_detail.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)
    
    @app.route('/movies/<int:id>', methods=["PATCH"])
    @requires_auth('update:movies')
    def update_movie(id):
        body = request.get_json()
        if not body:
            abort(422)
        
        try:
            movie = Movie.query.get(id)
        except:
            abort(404)
            
        movie.update()
        return jsonify({
            'success': True,
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date
        })
    """
    Error handler routes
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'request cannot be processed'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
