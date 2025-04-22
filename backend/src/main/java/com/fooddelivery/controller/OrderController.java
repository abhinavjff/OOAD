package com.fooddelivery.controller;

import com.fooddelivery.model.Order;
import com.fooddelivery.model.OrderItem;
import com.fooddelivery.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/orders")
@CrossOrigin(origins = "http://localhost:8502")
@RequiredArgsConstructor
public class OrderController {
    
    private final OrderService orderService;
    
    @GetMapping
    public ResponseEntity<?> getAllOrders() {
        try {
            List<Order> orders = orderService.getAllOrders();
            return ResponseEntity.ok(Map.of(
                "success", true,
                "orders", orders.stream().map(order -> Map.of(
                    "id", order.getId(),
                    "orderCode", order.getOrderCode(),
                    "restaurantName", order.getRestaurant().getName(),
                    "userName", order.getUser().getUsername(),
                    "totalAmount", order.getTotalAmount(),
                    "status", order.getStatus(),
                    "orderDate", order.getOrderDate()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/create")
    public ResponseEntity<?> createOrder(@RequestBody Map<String, Long> request) {
        try {
            Order order = orderService.createOrderFromCart(
                request.get("userId"),
                request.get("restaurantId")
            );
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Order created successfully",
                "order", Map.of(
                    "id", order.getId(),
                    "orderCode", order.getOrderCode(),
                    "totalAmount", order.getTotalAmount(),
                    "status", order.getStatus(),
                    "orderDate", order.getOrderDate()
                )
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @GetMapping("/user/{userId}")
    public ResponseEntity<?> getUserOrders(@PathVariable Long userId) {
        try {
            List<Order> orders = orderService.getUserOrders(userId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "orders", orders.stream().map(order -> Map.of(
                    "id", order.getId(),
                    "orderCode", order.getOrderCode(),
                    "restaurantName", order.getRestaurant().getName(),
                    "totalAmount", order.getTotalAmount(),
                    "status", order.getStatus(),
                    "orderDate", order.getOrderDate()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @GetMapping("/restaurant/{restaurantId}")
    public ResponseEntity<?> getRestaurantOrders(@PathVariable Long restaurantId) {
        try {
            List<Order> orders = orderService.getRestaurantOrders(restaurantId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "orders", orders.stream().map(order -> Map.of(
                    "id", order.getId(),
                    "orderCode", order.getOrderCode(),
                    "userName", order.getUser().getUsername(),
                    "totalAmount", order.getTotalAmount(),
                    "status", order.getStatus(),
                    "orderDate", order.getOrderDate()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @GetMapping("/{orderId}/items")
    public ResponseEntity<?> getOrderItems(@PathVariable Long orderId) {
        try {
            List<OrderItem> items = orderService.getOrderItems(orderId);
            return ResponseEntity.ok(Map.of(
                "success", true,
                "items", items.stream().map(item -> Map.of(
                    "id", item.getId(),
                    "menuItemName", item.getMenuItem().getName(),
                    "quantity", item.getQuantity(),
                    "price", item.getPrice()
                )).toList()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
    
    @PutMapping("/{orderId}/status")
    public ResponseEntity<?> updateOrderStatus(
            @PathVariable Long orderId,
            @RequestBody Map<String, String> request) {
        try {
            Order order = orderService.updateOrderStatus(orderId, request.get("status"));
            return ResponseEntity.ok(Map.of(
                "success", true,
                "message", "Order status updated successfully",
                "order", Map.of(
                    "id", order.getId(),
                    "orderCode", order.getOrderCode(),
                    "status", order.getStatus()
                )
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of(
                "success", false,
                "error", e.getMessage()
            ));
        }
    }
} 