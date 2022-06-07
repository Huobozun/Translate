import pandas as pd

from pubmed.db.db_models import Reference


class CitebyCalculator:
    def __init__(self, references: list, session=None) -> None:
        if session is None:
            from pubmed.db.db_engine import DbEngine

            self.session = DbEngine.session
        else:
            self.session = session
        self.references = references
        self._update_references(self.references)

    def get_citedby(self):
        df = pd.DataFrame(self.references)
        target_pmids = set(df["ref_to"].to_list())
        result = []
        refs = (
            self.session.query(Reference)
            .filter(Reference.ref_to.in_(target_pmids))
            .all()
        )
        refs_dict = [ref.to_dict() for ref in refs]
        target_refs = pd.DataFrame(refs_dict)
        for name, group in target_refs.groupby("ref_to"):
            result.append(
                {
                    "pmid": name,
                    "citedby_calculated": [x["ref_from"] for _, x in group.iterrows()],
                }
            )
        return result

    def _update_references(self, references: list):
        df = pd.DataFrame(references)
        ref_from = set(df["ref_from"].to_list())

        self.session.query(Reference).filter(Reference.ref_from.in_(ref_from)).delete(
            synchronize_session=False
        )
        self.session.commit()

        new_refs = [
            Reference(row["ref_from"], row["ref_to"]) for _, row in df.iterrows()
        ]
        self.session.add_all(new_refs)
        self.session.commit()
