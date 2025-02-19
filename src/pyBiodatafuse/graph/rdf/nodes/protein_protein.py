# protein_protein.py

"""Populate a BDF RDF graph with PPI nodes."""

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

from pyBiodatafuse.constants import BASE_URLS_DBS, NODE_TYPES, PREDICATES


def add_ppi_data(g: Graph, gene_node: URIRef, entry: dict, base_uri: str, new_uris: dict) -> URIRef:
    """Add a protein protein interaction node.

    :param g: RDFLib graph
    :param gene_node: URIRef for the target protein
    :param entry: the ppi dictionary
    :param base_uri: the base URI for the project
    :param new_uris: dictionary with project node URIs
    :return: a ppi URIRef node
    """
    gene_link = entry.get("stringdb_link_to", None)
    gene_link_node = URIRef(BASE_URLS_DBS["uniprot"] + gene_link)
    # ensembl = entry.get("Ensembl", None).split(":")[1]
    score = entry.get("score", None)
    uniprot = entry.get("Uniprot-TrEMBL", None)
    uniprot_link = entry.get("Uniprot-TrEMBL_link", None)
    if score:
        score = float(score)
        # Nodes
        ppi_node = URIRef(base_uri + f"ppi/{uniprot}_{gene_link_node}")
        # ensembl_node = URIRef(BASE_URLS_DBS["ensembl"] + f"{ensembl}")
        if uniprot:
            protein_node = URIRef(BASE_URLS_DBS["uniprot"] + uniprot)
            protein_link_node = URIRef(BASE_URLS_DBS["uniprot"] + uniprot_link)
            g.add((ppi_node, URIRef(PREDICATES["sio_has_part"]), protein_node))
            g.add((ppi_node, URIRef(PREDICATES["sio_has_part"]), protein_link_node))
            g.add((gene_node, URIRef(PREDICATES["translates_to"]), protein_node))
            g.add((protein_node, URIRef(PREDICATES["translation_of"]), gene_node))
            g.add((gene_link_node, URIRef(PREDICATES["translates_to"]), protein_link_node))
            g.add((protein_link_node, URIRef(PREDICATES["translation_of"]), gene_link_node))
            g.add((ppi_node, RDF.type, URIRef(NODE_TYPES["ppi_node"])))
            g.add((protein_link_node, RDF.type, URIRef(NODE_TYPES["protein_node"])))
            g.add((protein_node, RDF.type, URIRef(NODE_TYPES["protein_node"])))
            score_node = URIRef(f"{new_uris['score_base_node']}/{uniprot}_{uniprot_link}")
            g.add((score_node, RDF.type, URIRef(NODE_TYPES["score_node"])))
            g.add(
                (
                    score_node,
                    URIRef(PREDICATES["sio_has_value"]),
                    Literal(score, datatype=XSD.double),
                )
            )
            g.add((ppi_node, URIRef(PREDICATES["sio_has_measurement_value"]), score_node))

            return ppi_node
