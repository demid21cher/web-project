from flask import Flask
from flask_restful import Api, Resource, reqparse
import random

app = Flask(__name__)
api = Api(app)


questions = [
    {"id": 1, "question": "What is the capital of France?", "answer": "Paris"},
    {"id": 2, "question": "What is 2 + 2?", "answer": "4"},
    {
        "id": 3,
        "question": "What is the largest ocean on Earth?",
        "answer": "Pacific Ocean",
    },
    {"id": 4, "question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
    {"id": 5, "question": "What is the boiling point of water?", "answer": "100°C"},
]


class Questions(Resource):

    def get(self):
        return {"questions": questions}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "question", type=str, required=True, help="Question cannot be blank!"
        )

        parser.add_argument(
            "answer", type=str, required=True, help="Answer cannot be blank!"
        )

        data = parser.parse_args()

        new_question = {
            "id": len(questions) + 1,
            "question": data["question"],
            "answer": data["answer"],
        }

        questions.append(new_question)

        return {
            "message": "Question added successfully!",
            "question": new_question,
        }, 201


api.add_resource(Questions, "/questions")


class Question(Resource):
    def get(self, id):
        for question in questions:
            if question["id"] == id:
                return question, 200
        return {"message": "Question not found"}, 404

    def post(self, id):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "answer", type=str, required=True, help="Answer cannot be blank!"
        )

        data = parser.parse_args()

        for question in questions:
            if question["id"] == id:
                if question["answer"].lower() == data["answer"].lower():
                    return {"message": "Correct answer!"}, 200
                else:
                    return {"message": "Incorrect answer!"}, 200

        return {"message": "Question not found"}, 404


api.add_resource(Question, "/question/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
