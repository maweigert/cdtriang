#include <iostream>
#include <vector>
#include "CDT.h"

typedef float DTYPE;

typedef CDT::V2d<DTYPE> vertextype;


void _triangulate(const DTYPE * const vertices, const int n_vertices,
                  std::vector<std::vector<int> > &triangles){

  CDT::Triangulation<DTYPE> cdt(CDT::VertexInsertionOrder::AsProvided);
  
  std::vector<CDT::V2d<DTYPE>> cdt_vertices;
  
  for (int i = 0; i < n_vertices; ++i) 
    cdt_vertices.push_back(CDT::V2d<DTYPE>::make(vertices[2*i+1],vertices[2*i]));
  
  cdt.insertVertices(cdt_vertices);
  cdt.eraseSuperTriangle();

  for(const auto& tri: cdt.triangles) {

    std::vector<int> t;
    t.push_back(tri.vertices[0]);
    t.push_back(tri.vertices[1]);
    t.push_back(tri.vertices[2]);
    triangles.push_back(t);    
  }
}



void _triangulate_constrained(
                  const float * const vertices, const int n_vertices,
                  const int * const edges, const int n_edges,
                  std::vector<std::vector<int> > &triangles,
                  const bool remove_outer){

  // https://github.com/artem-ogre/CDT/issues/65
  CDT::Triangulation<DTYPE> cdt(CDT::VertexInsertionOrder::AsProvided);
  
  std::vector<CDT::V2d<DTYPE>> cdt_vertices;
  std::vector<CDT::Edge> cdt_edges;
  
  for (int i = 0; i < n_vertices; ++i) 
    cdt_vertices.push_back(CDT::V2d<DTYPE>::make(vertices[2*i+1],vertices[2*i]));

  for (int i = 0; i < n_edges; ++i) 
    cdt_edges.push_back(CDT::Edge(edges[2*i],edges[2*i+1]));
  
  
  cdt.insertVertices(cdt_vertices);
  cdt.insertEdges(cdt_edges);

  if (remove_outer){
    // cdt.eraseOuterTrianglesAndHoles();
    cdt.eraseOuterTriangles();
  }
  else
    cdt.eraseSuperTriangle();
  
  for(const auto& tri: cdt.triangles) {

    std::vector<int> t = {};
    t.push_back(tri.vertices[0]);
    t.push_back(tri.vertices[1]);
    t.push_back(tri.vertices[2]);
    triangles.push_back(t);    
  }

}
