# auth/verify.py
# import jwt
# import reflex as rx
# from ..backend.models import Usuario, Trabajador
# from ..backend.state import State
# from sqlmodel import select


# SECRET_KEY = "e85a85be384f74c22bbe0b93ba3404fe3ad75e2346c061c38ba4f77ea6971d35"




# def verify_account():       
        
#         jwt_token = State.token
#         if not isinstance(jwt_token, str):
#             print(f"Error: El token no es una cadena. Valor recibido: {jwt_token}")                   
    
#         try:
#             payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])

#             print(f"payload: {payload}")
#             user_id = payload['user_id']
#             user_type = payload['user_type']

#             with rx.session() as session:
#                 if user_type == 'usuario':
                    
#                     stmt = select(Usuario).where(Usuario.id == user_id)
#                     result = session.exec(stmt)
#                     user = result.one_or_none()
                    
#                     if user and not user.is_verified:
#                         user.is_verified = True
#                         session.commit()
#                         print("Usuario verificado con éxito.") 

#                 elif user_type == 'trabajador':                    
#                     stmt = select(Trabajador).where(Trabajador.id == user_id)
#                     result = session.exec(stmt)
#                     worker = result.one_or_none()
                    
#                     if worker and not worker.is_verified:
#                         worker.is_verified = True
#                         session.commit()
#                         print("Trabajador verificado con éxito.")
                        
#                 else:
#                      print("Tipo de usuario incorrecto en el token")

#         except jwt.ExpiredSignatureError:
#             print("El token ha expirado.")
           
#         except jwt.InvalidTokenError:
#             print("Token no válido.") 

    