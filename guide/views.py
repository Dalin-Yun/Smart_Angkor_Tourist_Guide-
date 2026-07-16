"""
----------------------------------------------------
Smart Angkor Tourist Guide
Views
----------------------------------------------------
Connects the ported HashTable / Graph / DecisionTree
algorithms to Django pages and a small JSON API used
by the interactive map (guide/static/guide/js/map.js).
----------------------------------------------------
"""

import json

from django.http import JsonResponse
from django.shortcuts import render

from .models import Temple, Road
from .algorithms.hash_table import HashTable
from .algorithms.graph import Graph
from .algorithms.decision_tree import recommend_tour
from .algorithms.utils import estimate_travel_time


# ---------- Builders: DB -> in-memory structures ----------

def build_hash_table():
    table = HashTable()
    for temple in Temple.objects.all():
        table.insert(temple.as_dict())
    return table


def build_graph():
    graph = Graph()
    for road in Road.objects.select_related("source", "destination").all():
        graph.add_edge(road.source.name, road.destination.name, road.distance)
    return graph


def graph_json():
    """Nodes/edges payload for the vis-network interactive map."""
    nodes = [
        {"id": t.name, "label": t.name, "category": t.category}
        for t in Temple.objects.all()
    ]
    edges = [
        {"from": r.source.name, "to": r.destination.name, "distance": r.distance}
        for r in Road.objects.select_related("source", "destination").all()
    ]
    return {"nodes": nodes, "edges": edges}


# ---------- Pages ----------

def home(request):
    return render(request, "guide/home.html", {
        "temple_count": Temple.objects.count(),
        "road_count": Road.objects.count(),
    })


def temple_list(request):

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    temples = Temple.objects.all()

    if query:
        temples = temples.filter(name__icontains=query)

    if category:
        temples = temples.filter(category=category)

    categories = (
        Temple.objects.order_by("category")
        .values_list("category", flat=True)
        .distinct()
    )

    return render(request, "guide/temple_list.html", {
        "temples": temples,
        "query": query,
        "category": category,
        "categories": categories,
    })


def temple_detail(request, temple_id):

    table = build_hash_table()
    temple = table.search_by_id(temple_id)

    return render(request, "guide/temple_detail.html", {
        "temple": temple,
        "found": temple is not None,
        "temple_id": temple_id,
    })


def navigation(request):
    """Interactive map page: pick start/end + algorithm, results via AJAX."""
    temples = Temple.objects.order_by("name")
    return render(request, "guide/navigation.html", {
        "temples": temples,
        "graph_data": json.dumps(graph_json()),
    })


def navigation_api(request):
    """
    JSON API backing the interactive map.
    ?algorithm=bfs|dfs|dijkstra&start=<name>&end=<name (dijkstra only)>
    """
    algorithm = request.GET.get("algorithm", "")
    start = request.GET.get("start", "").strip()
    end = request.GET.get("end", "").strip()

    graph = build_graph()

    if start not in graph.graph:
        return JsonResponse({"error": f"Start temple '{start}' not found."}, status=400)

    if algorithm == "bfs":
        order = graph.bfs(start)
        return JsonResponse({"algorithm": "bfs", "start": start, "order": order})

    elif algorithm == "dfs":
        order = graph.dfs(start)
        return JsonResponse({"algorithm": "dfs", "start": start, "order": order})

    elif algorithm == "dijkstra":

        if end not in graph.graph:
            return JsonResponse({"error": f"Destination temple '{end}' not found."}, status=400)

        path, distance = graph.dijkstra(start, end)

        if not path:
            return JsonResponse({"error": "No route found between these temples."}, status=404)

        return JsonResponse({
            "algorithm": "dijkstra",
            "start": start,
            "end": end,
            "path": path,
            "distance": round(distance, 2),
            "travel_time": estimate_travel_time(distance),
        })

    return JsonResponse({"error": "Unknown algorithm."}, status=400)


def recommend(request):

    time = request.GET.get("time", "")
    interest = request.GET.get("interest", "")

    recommend_list = []
    temples_info = []

    if time and interest:
        recommend_list = recommend_tour(time, interest)
        temples_info = Temple.objects.filter(name__in=recommend_list)

        # Keep the order returned by the decision tree
        order = {name: i for i, name in enumerate(recommend_list)}
        temples_info = sorted(temples_info, key=lambda t: order.get(t.name, 999))

    return render(request, "guide/recommend.html", {
        "time": time,
        "interest": interest,
        "temples_info": temples_info,
        "submitted": bool(time and interest),
    })
