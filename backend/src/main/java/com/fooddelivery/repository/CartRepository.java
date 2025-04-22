package com.fooddelivery.repository;

import com.fooddelivery.model.Cart;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CartRepository extends JpaRepository<Cart, Long> {
    List<Cart> findByUser_IdAndIsActiveTrue(Long userId);
    List<Cart> findByIsActiveTrue();
    Optional<Cart> findByUser_IdAndMenuItem_IdAndIsActiveTrue(Long userId, Long menuItemId);
    void deleteByUser_Id(Long userId);
} 