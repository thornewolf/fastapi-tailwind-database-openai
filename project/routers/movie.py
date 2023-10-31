import project.common as common
from project.llm import llm


@common.time_cache(3)
def get_movie(description: str, llm=llm):
    tries = 0
    response = 'BAD'*200
    while len(response) > 100:
        response = llm(f'''{description}''', system=f'''You are an AI that helps people find the movie they are looking for. They will provide you with a description of the movie and you will provide them with the title of the movie. User descriptions may be vague so always make a best effort guess. It's more important in this context to always return some guess than to tell the user they were vague. Limit all responses to just the movie name. If you provide any more content your response will be rejected.''', examples=[])
        tries += 1
        if tries > 2:
            return "Search failed. Please try again."
    return response
