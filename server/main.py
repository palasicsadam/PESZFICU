from website import create_app

app = create_app()

"""
num = 2
result = (num // 3) +1
print(result)
"""

if __name__ == "__main__":
    app.run(debug=True, port=5000)
