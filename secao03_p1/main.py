from typing import Optional, Any, List, Dict
from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends
from models import Curso
from fastapi.responses import JSONResponse
from time import sleep
from models import cursos


def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    finally:
        print("Fechando conexão com o banco de dados...")
        sleep(1)


app = FastAPI(title='API de Cursos da Geek University', version="0.0.1", description="Uma API para estudo do FastAPI")

@app.get('/cursos', description="Retorna todos os cursos ou uma lista vazia.", summary="Retorna todos os cursos", response_model=List[Curso], response_description="Cursos encontrados com sucesso")
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}', description="Retorna um dado especifico da lista de cursos", summary="Retorna um dado da lista")
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return curso

@app.post('/cursos', status_code=status.HTTP_201_CREATED, description="Inserir um novo dado para lista de cursos", summary="Inserir novo dado")
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put("/cursos/{curso_id}", description="Edita um dado especifico da lista de cursos", summary="Altera um dado")
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] =  curso
        del curso.id 
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um curso com id {curso_id}")


@app.delete("/cursos/{curso_id}", description="Deleta um dado especifico da lista de cursos", summary="Deleta um dado")
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um curso com id {curso_id}")


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int]= None, db: Any = Depends(fake_db)):
    soma : int = a + b

    if c:
        soma = soma + c
    
    print(f'X-GEEK: {x_geek}')

    return {"resultado": soma}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)