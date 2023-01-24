from fastapi import FastAPI, HTTPException, status

app = FastAPI()


cursos = {
    1: {
        "titulo": "Programação para leigos",
        "aulas": 112,
        "horas": 58
    },
    2: {
        "titulo": "Algoritmo e Logica de programação",
        "aulas": 87,
        "horas": 67
    }
}


@app.get('/cursos')
async def get_cursos():
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int):
    try:
        curso = cursos[curso_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return curso

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)