from pygetpapers import DownloadTools, EuropePmc
import requests
PAPERS = 'papers'
DOI = 'doi'


class PyLiteratureScore:
    def __init__(self) -> None:
        self.papers_metadata_dictionary = {}
        self.download_tools = DownloadTools()
        self.eupmc = EuropePmc()

    def query_pygetpapers(self, query, hits):
        print("querying pygetpapers")
        metadata_dictionary = self.eupmc.query(
            query, hits
        )
        return metadata_dictionary

    def get_doi_from_metadata_dictionary(self, metadata_dictionary):
        for paper in metadata_dictionary[PAPERS]:
            paper_metadata = metadata_dictionary[PAPERS][paper]
            if DOI in paper_metadata:
                self.papers_metadata_dictionary[paper] = {}
                self.papers_metadata_dictionary[paper][DOI] = paper_metadata[DOI]

    def query_openAlex_on_doi(self, my_doi):
        print(f"querying openalex for {my_doi}")
        try:
            url = "https://api.openalex.org/works/https://doi.org/"+my_doi
            specific_work = requests.get(url, timeout=5)
            return specific_work.json()
        except:
            return None

    def get_concepts_from_openAlexresult(self, openAlexResult, paper_id):
        if openAlexResult:
            openAlexConcepts = openAlexResult['concepts']
            self.papers_metadata_dictionary[paper_id]["concepts"] = openAlexConcepts

    def get_concepts_for_query(self, query, hits):
        hits = self.query_pygetpapers(query, hits)
        self.get_doi_from_metadata_dictionary(hits)
        for paper_id in self.papers_metadata_dictionary:
            paper_doi = self.papers_metadata_dictionary[paper_id]['doi']
            openAlexResult = self.query_openAlex_on_doi(paper_doi)
            self.get_concepts_from_openAlexresult(
                openAlexResult, paper_id)
        return self.papers_metadata_dictionary


def main():
    pyliteraturescore = PyLiteratureScore()
    doi_dictionary = pyliteraturescore.get_concepts_for_query("genes", 2)
    print(doi_dictionary)


if __name__ == "__main__":
    main()
