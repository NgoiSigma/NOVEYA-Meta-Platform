#ifndef NOVEA_ATOM_ENGINE_HPP
#define NOVEA_ATOM_ENGINE_HPP

#include <cmath>
#include <stdexcept>
#include <algorithm>

struct FDLMetrics {
    double nr_base;
    double nr_fact;
    double k_sn;
    double tr_true;
    int fdl_score;
};

class NoveaAtomEngine {
private:
    double shrine_pct = 0.10;
    double r_rate = 15.5;

public:
    NoveaAtomEngine() = default;
    FDLMetrics process_harvest_metrics(double t_base, double t_fact, double n_fe, double c_ch, double f_k) {
        if (n_fe <= 0.0) throw std::invalid_argument("Error: N_FE quantum must be strictly positive.");
        FDLMetrics metrics;
        metrics.nr_base = t_base / n_fe;
        metrics.nr_fact = t_fact / n_fe;
        metrics.k_sn = (metrics.nr_fact > 0.0) ? (metrics.nr_base / metrics.nr_fact) : 0.0;
        double denominator = c_ch - f_k;
        if (denominator <= 0.01) denominator = 0.01;
        metrics.tr_true = t_base / denominator;
        double base_score = (metrics.k_sn * 400.0) + (c_ch * 300.0) + (f_k * 100.0);
        metrics.fdl_score = std::clamp(static_cast<int>(base_score), 0, 1000);
        return metrics;
    }
};
#endif
